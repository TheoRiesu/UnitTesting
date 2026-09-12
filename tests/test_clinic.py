# Unit tests for the 5 required lab cases.
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from clinic.database import ClinicDatabase
from clinic.service import ClinicService


class TestClinic(unittest.TestCase):
    def setUp(self):
        # Fresh database for each test
        self.db = ClinicDatabase.get_instance()
        self.db.clear()
        self.service = ClinicService()
        self.service.owner_count = 0
        self.service.pet_count = 0
        self.service.appointment_count = 0

    # 1. Register Pet Owner
    def test_register_pet_owner(self):
        owner = self.service.register_owner("Ana", "0917-111")
        self.assertEqual(owner.name, "Ana")
        self.assertEqual(len(self.service.view_owners()), 1)

    # 2. Add Pet Record
    def test_add_pet_record(self):
        owner = self.service.register_owner("Ana", "0917-111")
        pet = self.service.add_pet("Bantay", "Dog", owner.owner_id)
        self.assertEqual(pet.species, "Dog")
        self.assertEqual(pet.owner_id, owner.owner_id)

    # 3. Schedule Appointment
    def test_schedule_appointment(self):
        owner = self.service.register_owner("Ana", "0917-111")
        pet = self.service.add_pet("Muning", "Cat", owner.owner_id)
        appt = self.service.schedule_appointment(pet.pet_id, "2026-09-20 10:30", "Checkup")
        self.assertEqual(appt.status, "Scheduled")
        self.assertEqual(len(self.service.view_appointments()), 1)

    # 4. Cancel Appointment
    def test_cancel_appointment(self):
        owner = self.service.register_owner("Ana", "0917-111")
        pet = self.service.add_pet("Tweety", "Bird", owner.owner_id)
        appt = self.service.schedule_appointment(pet.pet_id, "2026-09-20 11:00")
        result = self.service.cancel_appointment(appt.appointment_id)
        self.assertEqual(result.status, "Cancelled")

    # 5. Validate Singleton Instance
    def test_singleton_instance(self):
        db1 = ClinicDatabase.get_instance()
        db2 = ClinicDatabase()
        self.assertIs(db1, db2)


if __name__ == "__main__":
    unittest.main()
