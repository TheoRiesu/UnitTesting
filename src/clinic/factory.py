"""Factory Pattern for creating pets."""
from .models import Bird, Cat, Dog, Pet, Rabbit


class PetFactory:
    """Create pet objects from a type string.

    Supported types: Dog, Cat, Bird, Rabbit (case-insensitive).
    """

    SUPPORTED_TYPES = ("Dog", "Cat", "Bird", "Rabbit")

    _TYPE_MAP = {
        "dog": Dog,
        "cat": Cat,
        "bird": Bird,
        "rabbit": Rabbit,
    }

    @classmethod
    def create_pet(
        cls,
        pet_type: str,
        pet_id: str,
        name: str,
        owner_id: str,
        age: int = 0,
    ) -> Pet:
        """Create and return a Pet subclass instance.

        Raises:
            ValueError: if pet_type is not one of the supported types.
        """
        key = (pet_type or "").strip().lower()
        pet_class = cls._TYPE_MAP.get(key)
        if pet_class is None:
            raise ValueError(
                f"Unknown pet type '{pet_type}'. Supported: {', '.join(cls.SUPPORTED_TYPES)}"
            )
        return pet_class(pet_id=pet_id, name=name, owner_id=owner_id, age=age)

    @classmethod
    def supported_types(cls) -> tuple:
        return cls.SUPPORTED_TYPES
