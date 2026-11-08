from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.event_repository import EventRepository
from app.repositories.registration_repository import RegistrationRepository
from app.schemas.registration import RegistrationCreate, RegistrationResponse
from app.services.event_service import EventNotFoundError
from app.services.registration_service import (
    DuplicateRegistrationError,
    EventFullError,
    RegistrationNotFoundError,
    RegistrationService,
)

router = APIRouter(
    prefix="/events/{event_id}/registrations",
    tags=["registrations"],
)


def get_registration_service(
    session: Annotated[Session, Depends(get_db)],
) -> RegistrationService:
    return RegistrationService(
        EventRepository(session),
        RegistrationRepository(session),
    )


def event_not_found(error: EventNotFoundError) -> HTTPException:
    return HTTPException(status_code=404, detail=str(error))


@router.get("", response_model=list[RegistrationResponse])
def list_registrations(
    event_id: Annotated[int, Path(gt=0)],
    service: Annotated[RegistrationService, Depends(get_registration_service)],
) -> list[RegistrationResponse]:
    try:
        return service.list_for_event(event_id)
    except EventNotFoundError as error:
        raise event_not_found(error) from error


@router.post("", response_model=RegistrationResponse, status_code=201)
def create_registration(
    data: RegistrationCreate,
    event_id: Annotated[int, Path(gt=0)],
    service: Annotated[RegistrationService, Depends(get_registration_service)],
) -> RegistrationResponse:
    try:
        return service.register(event_id, data)
    except EventNotFoundError as error:
        raise event_not_found(error) from error
    except DuplicateRegistrationError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except EventFullError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.delete("/{registration_id}", status_code=204)
def cancel_registration(
    event_id: Annotated[int, Path(gt=0)],
    registration_id: Annotated[int, Path(gt=0)],
    service: Annotated[RegistrationService, Depends(get_registration_service)],
) -> Response:
    try:
        service.cancel(event_id, registration_id)
    except EventNotFoundError as error:
        raise event_not_found(error) from error
    except RegistrationNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return Response(status_code=204)
