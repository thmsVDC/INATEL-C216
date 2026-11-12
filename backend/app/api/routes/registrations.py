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


@router.get(
    "",
    response_model=list[RegistrationResponse],
    summary="Listar inscrições do evento",
    description=(
        "Retorna os participantes inscritos em um evento, na ordem em que "
        "fizeram a inscrição."
    ),
    response_description="Inscrições do evento.",
    responses={404: {"description": "Não existe evento com esse identificador."}},
)
def list_registrations(
    event_id: Annotated[int, Path(gt=0, description="Identificador do evento.")],
    service: Annotated[RegistrationService, Depends(get_registration_service)],
) -> list[RegistrationResponse]:
    try:
        return service.list_for_event(event_id)
    except EventNotFoundError as error:
        raise event_not_found(error) from error


@router.post(
    "",
    response_model=RegistrationResponse,
    status_code=201,
    summary="Inscrever participante",
    description=(
        "Cria uma inscrição para o evento. O e-mail é normalizado para evitar "
        "duplicidades. A API retorna `409` se o participante já estiver inscrito "
        "ou se todas as vagas estiverem ocupadas."
    ),
    response_description="Inscrição criada.",
    responses={
        404: {"description": "Não existe evento com esse identificador."},
        409: {"description": "E-mail já inscrito ou evento sem vagas."},
    },
)
def create_registration(
    data: RegistrationCreate,
    event_id: Annotated[int, Path(gt=0, description="Identificador do evento.")],
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


@router.delete(
    "/{registration_id}",
    status_code=204,
    summary="Cancelar inscrição",
    description=(
        "Cancela a inscrição e libera a vaga correspondente. O identificador "
        "da inscrição precisa pertencer ao evento informado."
    ),
    response_description="Inscrição cancelada com sucesso.",
    responses={
        404: {"description": "Evento ou inscrição não encontrado."},
    },
)
def cancel_registration(
    event_id: Annotated[int, Path(gt=0, description="Identificador do evento.")],
    registration_id: Annotated[
        int, Path(gt=0, description="Identificador da inscrição a cancelar.")
    ],
    service: Annotated[RegistrationService, Depends(get_registration_service)],
) -> Response:
    try:
        service.cancel(event_id, registration_id)
    except EventNotFoundError as error:
        raise event_not_found(error) from error
    except RegistrationNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return Response(status_code=204)
