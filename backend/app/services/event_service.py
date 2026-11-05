from datetime import datetime

from app.models import Event
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventUpdate


class EventNotFoundError(Exception):
    pass


class InvalidEventFilterError(Exception):
    pass


class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    def list_events(
        self,
        limit: int,
        offset: int,
        query: str | None = None,
        category: str | None = None,
        starts_after: datetime | None = None,
        starts_before: datetime | None = None,
    ) -> list[Event]:
        for date_filter in (starts_after, starts_before):
            if date_filter is not None and (
                date_filter.tzinfo is None or date_filter.utcoffset() is None
            ):
                raise InvalidEventFilterError(
                    "Informe as datas do filtro com fuso horário."
                )

        if (
            starts_after is not None
            and starts_before is not None
            and starts_after > starts_before
        ):
            raise InvalidEventFilterError(
                "A data inicial do filtro deve ser anterior à data final."
            )

        normalized_query = query.strip() if query and query.strip() else None
        normalized_category = (
            category.strip() if category and category.strip() else None
        )
        return self.repository.list(
            limit=limit,
            offset=offset,
            query=normalized_query,
            category=normalized_category,
            starts_after=starts_after,
            starts_before=starts_before,
        )

    def get_event(self, event_id: int) -> Event:
        event = self.repository.get(event_id)
        if event is None:
            raise EventNotFoundError(f"Evento {event_id} não encontrado.")
        return event

    def create_event(self, data: EventCreate) -> Event:
        event = Event(**data.model_dump())
        return self.repository.create(event)

    def update_event(self, event_id: int, data: EventUpdate) -> Event:
        event = self.get_event(event_id)
        for field, value in data.model_dump().items():
            setattr(event, field, value)
        return self.repository.save(event)

    def delete_event(self, event_id: int) -> None:
        self.repository.delete(self.get_event(event_id))
