from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventData(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=120,
        description="Nome público do evento.",
    )
    description: str | None = Field(
        default=None,
        max_length=3000,
        description="Apresentação do evento. Campo opcional.",
    )
    category: str = Field(
        min_length=1,
        max_length=60,
        description="Categoria usada para organizar e filtrar eventos.",
    )
    location: str = Field(
        min_length=1,
        max_length=150,
        description="Local físico ou endereço do evento.",
    )
    starts_at: datetime = Field(
        description="Data e hora de início em ISO 8601, incluindo o fuso horário."
    )
    capacity: int = Field(
        gt=0,
        le=10000,
        description="Número máximo de participantes permitidos.",
    )

    @field_validator("title", "category", "location")
    @classmethod
    def trim_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Este campo não pode ficar vazio.")
        return value

    @field_validator("description")
    @classmethod
    def trim_description(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None

    @field_validator("starts_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Informe a data e hora com fuso horário.")
        return value


class EventCreate(EventData):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Semana de Tecnologia",
                    "description": "Palestras e oficinas sobre inovação.",
                    "category": "Workshop",
                    "location": "Auditório principal",
                    "starts_at": "2026-11-20T09:00:00-03:00",
                    "capacity": 120,
                }
            ]
        }
    )


class EventUpdate(EventData):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Semana de Tecnologia 2026",
                    "description": "Palestras, oficinas e networking.",
                    "category": "Workshop",
                    "location": "Centro de convenções",
                    "starts_at": "2026-11-21T09:00:00-03:00",
                    "capacity": 150,
                }
            ]
        }
    )


class EventResponse(EventData):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Identificador único do evento.")
    created_at: datetime = Field(description="Data de criação do registro.")
