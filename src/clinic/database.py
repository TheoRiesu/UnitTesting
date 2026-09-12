# Singleton: only one ClinicDatabase object exists.

class ClinicDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.owners = {}
            cls._instance.pets = {}
            cls._instance.appointments = {}
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def clear(self):
        # Used in tests to start fresh
        self.owners = {}
        self.pets = {}
        self.appointments = {}
