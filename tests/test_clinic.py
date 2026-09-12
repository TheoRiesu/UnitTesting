import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from clinic.database import ClinicDatabase
from clinic.service import ClinicService


class TestClinic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._test_db = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "data-test.db")
        )
        ClinicDatabase.configure(cls._test_db)

    @classmethod
    def tearDownClass(cls):
        ClinicDatabase.reset_instance()
        for suffix in ("", "-wal", "-shm", "-journal"):
            try:
                os.remove(cls._test_db + suffix)
            except FileNotFoundError:
                pass
        ClinicDatabase.configure(None)

    def setUp(self):
        self.db = ClinicDatabase.get_instance()
        self.db.clear()
        self.service = ClinicService()

    def test_register_pet_owner(self):
        owner = self.service.register_owner("Ana", "0917-111")
        self.assertEqual(owner.name, "Ana")
        self.assertEqual(len(self.service.view_owners()), 1)

    def test_add_pet_record(self):
        owner = self.service.register_owner("Ana", "0917-111")
        pet = self.service.add_pet("Bantay", "Dog", owner.owner_id)
        self.assertEqual(pet.species, "Dog")
        self.assertEqual(pet.owner_id, owner.owner_id)

    def test_add_all_pet_types(self):
        owner = self.service.register_owner("Ana", "0917-111")
        for pet_type in ["Dog", "Cat", "Bird", "Rabbit"]:
            pet = self.service.add_pet("Pet-" + pet_type, pet_type, owner.owner_id)
            self.assertEqual(pet.species, pet_type)
            self.assertEqual(pet.owner_id, owner.owner_id)
        self.assertEqual(len(self.service.view_pets()), 4)

    def test_add_pet_invalid_type(self):
        owner = self.service.register_owner("Ana", "0917-111")
        with self.assertRaises(ValueError):
            self.service.add_pet("Fishy", "Fish", owner.owner_id)

    def test_add_pet_empty_name(self):
        owner = self.service.register_owner("Ana", "0917-111")
        with self.assertRaises(ValueError):
            self.service.add_pet("   ", "Dog", owner.owner_id)

    def test_schedule_appointment(self):
        owner = self.service.register_owner("Ana", "0917-111")
        pet = self.service.add_pet("Muning", "Cat", owner.owner_id)
        appt = self.service.schedule_appointment(pet.pet_id, "2026-09-20 10:30", "Checkup")
        self.assertEqual(appt.status, "Scheduled")
        self.assertEqual(len(self.service.view_appointments()), 1)

    def test_cancel_appointment(self):
        owner = self.service.register_owner("Ana", "0917-111")
        pet = self.service.add_pet("Tweety", "Bird", owner.owner_id)
        appt = self.service.schedule_appointment(pet.pet_id, "2026-09-20 11:00")
        result = self.service.cancel_appointment(appt.appointment_id)
        self.assertEqual(result.status, "Cancelled")

    def test_singleton_instance(self):
        db1 = ClinicDatabase.get_instance()
        db2 = ClinicDatabase()
        self.assertIs(db1, db2)

    def test_shared_id_sequence(self):
        other_service = ClinicService()
        owner1 = self.service.register_owner("Ana", "0917-111")
        owner2 = other_service.register_owner("Ben", "0917-222")
        self.assertNotEqual(owner1.owner_id, owner2.owner_id)
        self.assertEqual(owner1.owner_id, "O001")
        self.assertEqual(owner2.owner_id, "O002")

    def test_id_normalization(self):
        owner = self.service.register_owner("Aly", "0969900000")
        for trial in ["1", "0001", "O001", "o001", " O001 "]:
            pet = self.service.add_pet("Theo", "Dog", trial)
            self.assertEqual(pet.owner_id, owner.owner_id)
        appt = self.service.schedule_appointment("1", "2026-09-20 10:30")
        self.assertEqual(appt.pet_id, "P001")
        self.assertEqual(self.service.cancel_appointment("1").status, "Cancelled")
        self.assertEqual(
            self.service.update_status("a001", "completed").status, "Completed"
        )

    def test_persistence_across_restart(self):
        owner = self.service.register_owner("Persist", "0917-999")
        pet = self.service.add_pet("PersistPet", "Rabbit", owner.owner_id)
        appt = self.service.schedule_appointment(
            pet.pet_id, "2026-10-01 09:00", "Checkup"
        )
        ClinicDatabase.reset_instance()
        fresh_service = ClinicService()
        self.assertEqual(len(fresh_service.view_owners()), 1)
        self.assertEqual(fresh_service.view_owners()[0].name, "Persist")
        self.assertEqual(fresh_service.view_pets()[0].species, "Rabbit")
        self.assertEqual(
            fresh_service.view_appointments()[0].appointment_id,
            appt.appointment_id,
        )
        nxt = fresh_service.register_owner("Next", "0917-000")
        self.assertEqual(nxt.owner_id, "O002")


if __name__ == "__main__":
    unittest.main()
