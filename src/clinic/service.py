"""Application service: owner / pet / appointment use cases."""
from datetime import datetime
from typing import List

from .database import ClinicDatabase
from .factory import PetFactory
from .models import Appointment, AppointmentStatus, Owner, Pet

DATETIME_FORMAT = "%Y-%m-%d %H:%M"


class ClinicService:
    """Orchestrates ClinicDatabase + PetFactory with business rules."""

    def __init__(self, db: ClinicDatabase | None = None) -> None:
        self.db = db or ClinicDatabase.get_instance()
        self._owner_seq = 0
        self._pet_seq = 0
        self._appointment_seq = 0

    # -- Pet Owner Management --
    def register_owner(self, name: str, contact_number: str) -> Owner:
        if not name or not name.strip():
            raise ValueError("owner name must not be empty")
        if not contact_number or not contact_number.strip():
            raise ValueError("contact number must not be empty")
        for existing in self.db.list_owners():
            if existing.contact_number == contact_number.strip():
                raise ValueError(f"contact number '{contact_number}' already registered")
        self._owner_seq += 1
        owner = Owner(
            owner_id=f"O{self._owner_seq:03d}",
            name=name.strip(),
            contact_number=contact_number.strip(),
        )
        self.db.add_owner(owner)
        return owner

    def view_owners(self) -> List[Owner]:
        return self.db.list_owners()

    # -- Pet Management --
    def add_pet(self, name: str, pet_type: str, owner_id: str, age: int = 0) -> Pet:
        if self.db.get_owner(owner_id) is None:
            raise ValueError(f"owner_id '{owner_id}' not found")
        self._pet_seq += 1
        pet = PetFactory.create_pet(
            pet_type=pet_type,
            pet_id=f"P{self._pet_seq:03d}",
            name=name.strip(),
            owner_id=owner_id,
            age=age,
        )
        self.db.add_pet(pet)
        return pet

    def view_pets(self, owner_id: str | None = None) -> List[Pet]:
        if owner_id:
            return self.db.list_pets_by_owner(owner_id)
        return self.db.list_pets()

    # -- Appointment Management --
    @staticmethod
    def parse_datetime(value: str) -> datetime:
        try:
            return datetime.strptime(value.strip(), DATETIME_FORMAT)
        except ValueError as exc:
            raise ValueError(f"Use format YYYY-MM-DD HH:MM (e.g. 2026-09-20 10:00)") from exc

    def schedule_appointment(self, pet_id: str, date_time_str: str, reason: str = "") -> Appointment:
        pet = self.db.get_pet(pet_id)
        if pet is None:
            raise ValueError(f"pet_id '{pet_id}' not found")
        date_time = self.parse_datetime(date_time_str)
        # Prevent scheduling conflicts: same pet, same slot, still active.
        for appt in self.db.list_appointments():
            if (
                appt.pet_id == pet_id
                and appt.date_time == date_time
                and appt.status == AppointmentStatus.SCHEDULED
            ):
                raise ValueError(f"pet '{pet_id}' already has an active appointment at {date_time_str}")
        self._appointment_seq += 1
        appointment = Appointment(
            appointment_id=f"A{self._appointment_seq:03d}",
            pet_id=pet_id,
            owner_id=pet.owner_id,
            date_time=date_time,
            reason=reason.strip(),
            status=AppointmentStatus.SCHEDULED,
        )
        self.db.add_appointment(appointment)
        return appointment

    def view_appointments(self) -> List[Appointment]:
        return sorted(self.db.list_appointments(), key=lambda a: a.date_time)

    def cancel_appointment(self, appointment_id: str) -> Appointment:
        appt = self.db.get_appointment(appointment_id)
        if appt is None:
            raise ValueError(f"appointment_id '{appointment_id}' not found")
        if appt.status == AppointmentStatus.CANCELLED:
            raise ValueError(f"appointment '{appointment_id}' is already cancelled")
        if appt.status == AppointmentStatus.COMPLETED:
            raise ValueError(f"completed appointment '{appointment_id}' cannot be cancelled")
        appt.status = AppointmentStatus.CANCELLED
        return appt

    def update_appointment_status(self, appointment_id: str, status: str) -> Appointment:
        appt = self.db.get_appointment(appointment_id)
        if appt is None:
            raise ValueError(f"appointment_id '{appointment_id}' not found")
        try:
            appt.status = AppointmentStatus(status)
        except ValueError as exc:
            valid = ", ".join(s.value for s in AppointmentStatus)
            raise ValueError(f"Invalid status '{status}'. Use: {valid}") from exc
        return appt
