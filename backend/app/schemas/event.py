from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventData(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=3000)
    category: str = Field(min_length=1, max_length=60)
    location: str = Field(min_length=1, max_length=150)
    starts_at: datetime
    capacity: int = Field(gt=0, le=10000)

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
    pass


class EventUpdate(EventData):
    pass


class EventResponse(EventData):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
