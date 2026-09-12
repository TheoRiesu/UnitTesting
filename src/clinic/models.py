"""Domain models: Owner, Pet hierarchy, Appointment."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


@dataclass
class Owner:
    """Pet owner record: Owner ID, Name, Contact Number."""

    owner_id: str
    name: str
    contact_number: str

    def __post_init__(self) -> None:
        if not self.owner_id or not self.owner_id.strip():
            raise ValueError("owner_id must not be empty")
        if not self.name or not self.name.strip():
            raise ValueError("name must not be empty")
        if not self.contact_number or not self.contact_number.strip():
            raise ValueError("contact_number must not be empty")

    def __str__(self) -> str:
        return f"{self.owner_id}: {self.name} ({self.contact_number})"


@dataclass
class Pet:
    """Base pet record. Created via PetFactory; do not instantiate directly for unknown types."""

    pet_id: str
    name: str
    owner_id: str
    age: int = 0
    species: str = field(default="Unknown", init=False)

    def __post_init__(self) -> None:
        if not self.pet_id or not self.pet_id.strip():
            raise ValueError("pet_id must not be empty")
        if not self.name or not self.name.strip():
            raise ValueError("pet name must not be empty")
        if not self.owner_id or not self.owner_id.strip():
            raise ValueError("owner_id must not be empty")
        if self.age < 0:
            raise ValueError("age must be >= 0")

    @property
    def sound(self) -> str:
        return "..."

    def __str__(self) -> str:
        return f"{self.pet_id}: {self.name} [{self.species}] (owner={self.owner_id})"


@dataclass
class Dog(Pet):
    species: str = field(default="Dog", init=False)

    @property
    def sound(self) -> str:
        return "Woof!"


@dataclass
class Cat(Pet):
    species: str = field(default="Cat", init=False)

    @property
    def sound(self) -> str:
        return "Meow!"


@dataclass
class Bird(Pet):
    species: str = field(default="Bird", init=False)

    @property
    def sound(self) -> str:
        return "Chirp!"


@dataclass
class Rabbit(Pet):
    species: str = field(default="Rabbit", init=False)

    @property
    def sound(self) -> str:
        return "Squeak!"


class AppointmentStatus(str, Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


@dataclass
class Appointment:
    """Appointment record linking a pet (and its owner) to a date/time."""

    appointment_id: str
    pet_id: str
    owner_id: str
    date_time: datetime
    reason: str = ""
    status: AppointmentStatus = AppointmentStatus.SCHEDULED

    def __post_init__(self) -> None:
        if not self.appointment_id or not self.appointment_id.strip():
            raise ValueError("appointment_id must not be empty")
        if not self.pet_id or not self.pet_id.strip():
            raise ValueError("pet_id must not be empty")
        if not self.owner_id or not self.owner_id.strip():
            raise ValueError("owner_id must not be empty")
        if isinstance(self.status, str):
            # Allow plain strings like "Scheduled" for convenience.
            self.status = AppointmentStatus(self.status)

    def __str__(self) -> str:
        dt = self.date_time.strftime("%Y-%m-%d %H:%M")
        return f"{self.appointment_id}: pet={self.pet_id} at {dt} [{self.status.value}]"
