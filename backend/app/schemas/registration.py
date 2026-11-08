from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RegistrationCreate(BaseModel):
    participant_name: str = Field(min_length=2, max_length=120)
    participant_email: str = Field(
        min_length=6,
        max_length=254,
        pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
    )

    @field_validator("participant_name")
    @classmethod
    def trim_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Informe o nome do participante.")
        return value

    @field_validator("participant_email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().casefold()


class RegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    participant_name: str
    participant_email: str
    registered_at: datetime
