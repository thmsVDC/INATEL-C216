from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Registration


class RegistrationConflictError(Exception):
    pass


class RegistrationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_for_event(self, event_id: int) -> list[Registration]:
        statement = (
            select(Registration)
            .where(Registration.event_id == event_id)
            .order_by(Registration.registered_at.asc(), Registration.id.asc())
        )
        return list(self.session.scalars(statement).all())

    def count_for_event(self, event_id: int) -> int:
        statement = select(func.count()).select_from(Registration).where(
            Registration.event_id == event_id
        )
        return self.session.scalar(statement) or 0

    def get_by_email(self, event_id: int, email: str) -> Registration | None:
        statement = select(Registration).where(
            Registration.event_id == event_id,
            Registration.participant_email == email,
        )
        return self.session.scalar(statement)

    def get(self, event_id: int, registration_id: int) -> Registration | None:
        statement = select(Registration).where(
            Registration.event_id == event_id,
            Registration.id == registration_id,
        )
        return self.session.scalar(statement)

    def create(self, registration: Registration) -> Registration:
        self.session.add(registration)
        try:
            self.session.commit()
        except IntegrityError as error:
            self.session.rollback()
            raise RegistrationConflictError from error
        self.session.refresh(registration)
        return registration

    def delete(self, registration: Registration) -> None:
        self.session.delete(registration)
        self.session.commit()
