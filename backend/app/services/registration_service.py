from app.models import Event, Registration
from app.repositories.event_repository import EventRepository
from app.repositories.registration_repository import (
    RegistrationConflictError,
    RegistrationRepository,
)
from app.schemas.registration import RegistrationCreate
from app.services.event_service import EventNotFoundError


class EventFullError(Exception):
    pass


class DuplicateRegistrationError(Exception):
    pass


class RegistrationNotFoundError(Exception):
    pass


class RegistrationService:
    def __init__(
        self,
        event_repository: EventRepository,
        registration_repository: RegistrationRepository,
    ) -> None:
        self.event_repository = event_repository
        self.registration_repository = registration_repository

    def list_for_event(self, event_id: int) -> list[Registration]:
        self._get_event(event_id)
        return self.registration_repository.list_for_event(event_id)

    def register(
        self, event_id: int, data: RegistrationCreate
    ) -> Registration:
        event = self._get_event(event_id, lock=True)
        email = data.participant_email

        if self.registration_repository.get_by_email(event_id, email) is not None:
            raise DuplicateRegistrationError(
                "Este e-mail já está inscrito neste evento."
            )

        if self.registration_repository.count_for_event(event_id) >= event.capacity:
            raise EventFullError("Este evento não tem mais vagas disponíveis.")

        registration = Registration(
            event_id=event_id,
            participant_name=data.participant_name,
            participant_email=email,
        )
        try:
            return self.registration_repository.create(registration)
        except RegistrationConflictError as error:
            raise DuplicateRegistrationError(
                "Este e-mail já está inscrito neste evento."
            ) from error

    def cancel(self, event_id: int, registration_id: int) -> None:
        self._get_event(event_id)
        registration = self.registration_repository.get(event_id, registration_id)
        if registration is None:
            raise RegistrationNotFoundError(
                f"Inscrição {registration_id} não encontrada para este evento."
            )
        self.registration_repository.delete(registration)

    def _get_event(self, event_id: int, lock: bool = False) -> Event:
        event = (
            self.event_repository.get_for_update(event_id)
            if lock
            else self.event_repository.get(event_id)
        )
        if event is None:
            raise EventNotFoundError(f"Evento {event_id} não encontrado.")
        return event
