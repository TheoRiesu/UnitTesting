"""Singleton in-memory clinic database."""
from typing import Dict, List, Optional

from .models import Appointment, Owner, Pet


class ClinicDatabase:
    """Single shared in-memory store for owners, pets, and appointments.

    Singleton Pattern: only one instance ever exists, accessed via
    ``ClinicDatabase.get_instance()`` (or plain ``ClinicDatabase()``).
    """

    _instance: Optional["ClinicDatabase"] = None

    def __new__(cls) -> "ClinicDatabase":
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instance = instance
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        self.owners: Dict[str, Owner] = {}
        self.pets: Dict[str, Pet] = {}
        self.appointments: Dict[str, Appointment] = {}
        self._initialized = True

    @classmethod
    def get_instance(cls) -> "ClinicDatabase":
        return cls()

    # -- test/lifecycle helpers --
    def clear(self) -> None:
        """Remove all records (used to isolate unit tests and demos)."""
        self.owners.clear()
        self.pets.clear()
        self.appointments.clear()

    # -- owner records --
    def add_owner(self, owner: Owner) -> None:
        if owner.owner_id in self.owners:
            raise ValueError(f"owner_id '{owner.owner_id}' already exists")
        self.owners[owner.owner_id] = owner

    def get_owner(self, owner_id: str) -> Optional[Owner]:
        return self.owners.get(owner_id)

    def list_owners(self) -> List[Owner]:
        return list(self.owners.values())

    # -- pet records --
    def add_pet(self, pet: Pet) -> None:
        if pet.pet_id in self.pets:
            raise ValueError(f"pet_id '{pet.pet_id}' already exists")
        self.pets[pet.pet_id] = pet

    def get_pet(self, pet_id: str) -> Optional[Pet]:
        return self.pets.get(pet_id)

    def list_pets(self) -> List[Pet]:
        return list(self.pets.values())

    def list_pets_by_owner(self, owner_id: str) -> List[Pet]:
        return [p for p in self.pets.values() if p.owner_id == owner_id]

    # -- appointment records --
    def add_appointment(self, appointment: Appointment) -> None:
        if appointment.appointment_id in self.appointments:
            raise ValueError(f"appointment_id '{appointment.appointment_id}' already exists")
        self.appointments[appointment.appointment_id] = appointment

    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        return self.appointments.get(appointment_id)

    def list_appointments(self) -> List[Appointment]:
        return list(self.appointments.values())
