from .database import ClinicDatabase
from .factory import PetFactory
from .models import Owner, Appointment


class ClinicService:
    def __init__(self):
        self.db = ClinicDatabase.get_instance()

    @staticmethod
    def _normalize_id(raw_id, prefix):
        s = str(raw_id).strip().upper()
        num = s[len(prefix):].strip() if s.startswith(prefix) else s
        if num.isdigit():
            return prefix + str(int(num)).zfill(3)
        return s

    def register_owner(self, name, contact_number):
        if name.strip() == "":
            raise ValueError("Name cannot be empty")
        if contact_number.strip() == "":
            raise ValueError("Contact cannot be empty")
        owner_id = self.db.next_owner_id()
        owner = Owner(owner_id, name, contact_number)
        self.db.save_owner(owner)
        return owner

    def view_owners(self):
        return list(self.db.owners.values())

    def add_pet(self, name, pet_type, owner_id, age=0):
        if name.strip() == "":
            raise ValueError("Pet name cannot be empty")
        owner_id = self._normalize_id(owner_id, "O")
        if owner_id not in self.db.owners:
            raise ValueError("Owner not found: " + owner_id)
        pet_type = str(pet_type).strip()
        if pet_type.lower() not in ("dog", "cat", "bird", "rabbit"):
            raise ValueError("Unknown pet type: " + pet_type)
        pet_id = self.db.next_pet_id()
        pet = PetFactory.create_pet(pet_type, pet_id, name, owner_id, age)
        self.db.save_pet(pet)
        return pet

    def view_pets(self):
        return list(self.db.pets.values())

    def schedule_appointment(self, pet_id, date_time, reason=""):
        pet_id = self._normalize_id(pet_id, "P")
        if pet_id not in self.db.pets:
            raise ValueError("Pet not found: " + pet_id)
        for a in self.db.appointments.values():
            if a.pet_id == pet_id and a.date_time == date_time and a.status == "Scheduled":
                raise ValueError("Pet already booked at that time")
        appointment_id = self.db.next_appointment_id()
        pet = self.db.pets[pet_id]
        appt = Appointment(appointment_id, pet_id, pet.owner_id, date_time, reason)
        self.db.save_appointment(appt)
        return appt

    def view_appointments(self):
        return list(self.db.appointments.values())

    def cancel_appointment(self, appointment_id):
        appointment_id = self._normalize_id(appointment_id, "A")
        if appointment_id not in self.db.appointments:
            raise ValueError("Appointment not found")
        appt = self.db.appointments[appointment_id]
        appt.status = "Cancelled"
        self.db.save_appointment(appt)
        return appt

    def update_status(self, appointment_id, status):
        appointment_id = self._normalize_id(appointment_id, "A")
        status = str(status).strip().capitalize()
        if status not in ["Scheduled", "Completed", "Cancelled"]:
            raise ValueError("Bad status: " + status)
        if appointment_id not in self.db.appointments:
            raise ValueError("Appointment not found")
        appt = self.db.appointments[appointment_id]
        appt.status = status
        self.db.save_appointment(appt)
        return appt
