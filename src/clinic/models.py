# Simple data classes for the vet clinic.

class Owner:
    def __init__(self, owner_id, name, contact_number):
        self.owner_id = owner_id
        self.name = name
        self.contact_number = contact_number

    def __str__(self):
        return self.owner_id + ": " + self.name + " (" + self.contact_number + ")"


class Pet:
    def __init__(self, pet_id, name, owner_id, age=0):
        self.pet_id = pet_id
        self.name = name
        self.owner_id = owner_id
        self.age = age
        self.species = "Pet"

    def __str__(self):
        return self.pet_id + ": " + self.name + " [" + self.species + "]"


class Dog(Pet):
    def __init__(self, pet_id, name, owner_id, age=0):
        super().__init__(pet_id, name, owner_id, age)
        self.species = "Dog"


class Cat(Pet):
    def __init__(self, pet_id, name, owner_id, age=0):
        super().__init__(pet_id, name, owner_id, age)
        self.species = "Cat"


class Bird(Pet):
    def __init__(self, pet_id, name, owner_id, age=0):
        super().__init__(pet_id, name, owner_id, age)
        self.species = "Bird"


class Rabbit(Pet):
    def __init__(self, pet_id, name, owner_id, age=0):
        super().__init__(pet_id, name, owner_id, age)
        self.species = "Rabbit"


class Appointment:
    def __init__(self, appointment_id, pet_id, owner_id, date_time, reason=""):
        self.appointment_id = appointment_id
        self.pet_id = pet_id
        self.owner_id = owner_id
        self.date_time = date_time
        self.reason = reason
        self.status = "Scheduled"  # Scheduled, Completed, Cancelled

    def __str__(self):
        return (
            self.appointment_id + ": pet=" + self.pet_id
            + " at " + self.date_time
            + " [" + self.status + "]"
        )
