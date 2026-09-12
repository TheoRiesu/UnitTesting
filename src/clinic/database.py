# Singleton: only one ClinicDatabase object exists.
# ID counters live here so all ClinicService instances share one sequence.

class ClinicDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.owners = {}
            cls._instance.pets = {}
            cls._instance.appointments = {}
            cls._instance.owner_seq = 0
            cls._instance.pet_seq = 0
            cls._instance.appointment_seq = 0
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def clear(self):
        # Used in tests to start fresh
        self.owners = {}
        self.pets = {}
        self.appointments = {}
        self.owner_seq = 0
        self.pet_seq = 0
        self.appointment_seq = 0

    def next_owner_id(self):
        self.owner_seq += 1
        return "O" + str(self.owner_seq).zfill(3)

    def next_pet_id(self):
        self.pet_seq += 1
        return "P" + str(self.pet_seq).zfill(3)

    def next_appointment_id(self):
        self.appointment_seq += 1
        return "A" + str(self.appointment_seq).zfill(3)
