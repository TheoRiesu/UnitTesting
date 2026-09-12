# Factory: creates the right pet object by type name.
from .models import Dog, Cat, Bird, Rabbit


class PetFactory:
    @staticmethod
    def create_pet(pet_type, pet_id, name, owner_id, age=0):
        pet_type = pet_type.lower()
        if pet_type == "dog":
            return Dog(pet_id, name, owner_id, age)
        elif pet_type == "cat":
            return Cat(pet_id, name, owner_id, age)
        elif pet_type == "bird":
            return Bird(pet_id, name, owner_id, age)
        elif pet_type == "rabbit":
            return Rabbit(pet_id, name, owner_id, age)
        else:
            raise ValueError("Unknown pet type: " + pet_type)
