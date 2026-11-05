from app.models import Event
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventUpdate


class EventNotFoundError(Exception):
    pass


class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    def list_events(self, limit: int, offset: int) -> list[Event]:
        return self.repository.list(limit, offset)

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
