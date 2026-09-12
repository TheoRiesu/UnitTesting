# Simple service with all clinic actions.
from .database import ClinicDatabase
from .factory import PetFactory
from .models import Owner, Appointment


class ClinicService:
    def __init__(self):
        self.db = ClinicDatabase.get_instance()

    # 1. Pet Owner Management
    def register_owner(self, name, contact_number):
        if name.strip() == "":
            raise ValueError("Name cannot be empty")
        if contact_number.strip() == "":
            raise ValueError("Contact cannot be empty")
        owner_id = self.db.next_owner_id()
        owner = Owner(owner_id, name, contact_number)
        self.db.owners[owner_id] = owner
        return owner

    def view_owners(self):
        return list(self.db.owners.values())

    # 2. Pet Management
    def add_pet(self, name, pet_type, owner_id, age=0):
        if name.strip() == "":
            raise ValueError("Pet name cannot be empty")
        if owner_id not in self.db.owners:
            raise ValueError("Owner not found: " + owner_id)
        if pet_type.lower() not in ("dog", "cat", "bird", "rabbit"):
            raise ValueError("Unknown pet type: " + pet_type)
        pet_id = self.db.next_pet_id()
        pet = PetFactory.create_pet(pet_type, pet_id, name, owner_id, age)
        self.db.pets[pet_id] = pet
        return pet

    def view_pets(self):
        return list(self.db.pets.values())

    # 3. Appointment Management
    def schedule_appointment(self, pet_id, date_time, reason=""):
        if pet_id not in self.db.pets:
            raise ValueError("Pet not found: " + pet_id)
        # Avoid double booking same pet + same time
        for a in self.db.appointments.values():
            if a.pet_id == pet_id and a.date_time == date_time and a.status == "Scheduled":
                raise ValueError("Pet already booked at that time")
        appointment_id = self.db.next_appointment_id()
        pet = self.db.pets[pet_id]
        appt = Appointment(appointment_id, pet_id, pet.owner_id, date_time, reason)
        self.db.appointments[appointment_id] = appt
        return appt

    def view_appointments(self):
        return list(self.db.appointments.values())

    def cancel_appointment(self, appointment_id):
        if appointment_id not in self.db.appointments:
            raise ValueError("Appointment not found")
        appt = self.db.appointments[appointment_id]
        appt.status = "Cancelled"
        return appt

    def update_status(self, appointment_id, status):
        if status not in ["Scheduled", "Completed", "Cancelled"]:
            raise ValueError("Bad status: " + status)
        if appointment_id not in self.db.appointments:
            raise ValueError("Appointment not found")
        appt = self.db.appointments[appointment_id]
        appt.status = status
        return appt
