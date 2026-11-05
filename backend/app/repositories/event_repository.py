from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Event


class EventRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, limit: int, offset: int) -> list[Event]:
        statement = (
            select(Event)
            .order_by(Event.starts_at.asc(), Event.id.asc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(statement).all())

    def get(self, event_id: int) -> Event | None:
        return self.session.get(Event, event_id)

    def create(self, event: Event) -> Event:
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def save(self, event: Event) -> Event:
        self.session.commit()
        self.session.refresh(event)
        return event

    def delete(self, event: Event) -> None:
        self.session.delete(event)
        self.session.commit()
