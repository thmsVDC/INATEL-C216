from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Event


class EventRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(
        self,
        limit: int,
        offset: int,
        query: str | None,
        category: str | None,
        starts_after: datetime | None,
        starts_before: datetime | None,
    ) -> list[Event]:
        statement = select(Event)
        if query:
            statement = statement.where(
                func.lower(Event.title).contains(query.lower(), autoescape=True)
            )
        if category:
            statement = statement.where(func.lower(Event.category) == category.lower())
        if starts_after:
            statement = statement.where(Event.starts_at >= starts_after)
        if starts_before:
            statement = statement.where(Event.starts_at <= starts_before)

        statement = statement.order_by(Event.starts_at.asc(), Event.id.asc())
        statement = statement.offset(offset).limit(limit)
        return list(self.session.scalars(statement).all())

    def get(self, event_id: int) -> Event | None:
        return self.session.get(Event, event_id)

    def get_for_update(self, event_id: int) -> Event | None:
        statement = select(Event).where(Event.id == event_id).with_for_update()
        return self.session.scalar(statement)

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
