from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RegistrationCreate(BaseModel):
    participant_name: str = Field(
        min_length=2,
        max_length=120,
        description="Nome completo do participante.",
    )
    participant_email: str = Field(
        min_length=6,
        max_length=254,
        pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        description="E-mail usado para identificar uma inscrição por evento.",
    )
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "participant_name": "Ana Souza",
                    "participant_email": "ana.souza@example.com",
                }
            ]
        }
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

    id: int = Field(description="Identificador único da inscrição.")
    event_id: int = Field(description="Identificador do evento associado.")
    participant_name: str = Field(description="Nome informado pelo participante.")
    participant_email: str = Field(description="E-mail normalizado do participante.")
    registered_at: datetime = Field(
        description="Data e hora em que a inscrição foi feita."
    )
