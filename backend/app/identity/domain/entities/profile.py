from datetime import date
from uuid import UUID, uuid4

from app.identity.domain.enums.gender import Gender


class Profile:
    def __init__(
        self,
        user_id: UUID,
        first_name: str,
        birth_date: date,
        gender: Gender,
        bio: str | None = None,
        profile_id: UUID | None = None,
    ):
        self._validate_first_name(first_name)

        self.id = profile_id or uuid4()
        self.user_id = user_id
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.bio = bio

    @staticmethod
    def _validate_first_name(first_name: str) -> None:
        if not first_name.strip():
            raise ValueError("First name cannot be empty.")

        if len(first_name) > 100:
            raise ValueError("First name cannot exceed 100 characters.")