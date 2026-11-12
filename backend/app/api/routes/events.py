from collections.abc import Sequence
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.services.event_service import (
    EventNotFoundError,
    EventService,
    InvalidEventFilterError,
)

router = APIRouter(prefix="/events", tags=["events"])


def get_event_service(
    session: Annotated[Session, Depends(get_db)],
) -> EventService:
    return EventService(EventRepository(session))


def not_found(error: EventNotFoundError) -> HTTPException:
    return HTTPException(status_code=404, detail=str(error))


@router.get(
    "",
    response_model=list[EventResponse],
    summary="Listar eventos",
    description=(
        "Retorna eventos ordenados pela data de início. Você pode combinar "
        "busca por título, categoria, período e paginação. As datas devem usar "
        "ISO 8601 com fuso horário, por exemplo `2026-11-20T09:00:00-03:00`."
    ),
    response_description="Eventos encontrados para os filtros informados.",
    responses={
        422: {
            "description": "Filtros inválidos ou período com datas inconsistentes."
        }
    },
)
def list_events(
    service: Annotated[EventService, Depends(get_event_service)],
    limit: Annotated[
        int,
        Query(ge=1, le=100, description="Quantidade máxima de eventos por página."),
    ] = 50,
    offset: Annotated[
        int, Query(ge=0, description="Quantidade de eventos ignorados no início.")
    ] = 0,
    query: Annotated[
        str | None,
        Query(alias="q", max_length=120, description="Trecho do título do evento."),
    ] = None,
    category: Annotated[
        str | None, Query(max_length=60, description="Categoria exata do evento.")
    ] = None,
    starts_after: Annotated[
        datetime | None,
        Query(
            description="Início do período, inclusivo, em ISO 8601 com fuso horário."
        ),
    ] = None,
    starts_before: Annotated[
        datetime | None,
        Query(description="Fim do período, inclusivo, em ISO 8601 com fuso horário."),
    ] = None,
) -> Sequence[EventResponse]:
    try:
        return service.list_events(
            limit=limit,
            offset=offset,
            query=query,
            category=category,
            starts_after=starts_after,
            starts_before=starts_before,
        )
    except InvalidEventFilterError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Consultar evento",
    description="Busca os detalhes de um evento pelo identificador.",
    response_description="Dados completos do evento.",
    responses={404: {"description": "Não existe evento com esse identificador."}},
)
def get_event(
    event_id: Annotated[int, Path(gt=0, description="Identificador do evento.")],
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventResponse:
    try:
        return service.get_event(event_id)
    except EventNotFoundError as error:
        raise not_found(error) from error


@router.post(
    "",
    response_model=EventResponse,
    status_code=201,
    summary="Criar evento",
    description=(
        "Cadastra um evento e retorna o registro criado. A data deve incluir "
        "fuso horário e a capacidade precisa ser maior que zero."
    ),
    response_description="Evento criado.",
)
def create_event(
    data: EventCreate,
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventResponse:
    return service.create_event(data)


@router.put(
    "/{event_id}",
    response_model=EventResponse,
    summary="Atualizar evento",
    description=(
        "Substitui integralmente os dados editáveis de um evento. Envie todos "
        "os campos exigidos no corpo da requisição."
    ),
    response_description="Evento atualizado.",
    responses={404: {"description": "Não existe evento com esse identificador."}},
)
def update_event(
    data: EventUpdate,
    event_id: Annotated[int, Path(gt=0, description="Identificador do evento.")],
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventResponse:
    try:
        return service.update_event(event_id, data)
    except EventNotFoundError as error:
        raise not_found(error) from error


@router.delete(
    "/{event_id}",
    status_code=204,
    summary="Excluir evento",
    description=(
        "Remove o evento. As inscrições associadas também são removidas. "
        "A operação não retorna conteúdo."
    ),
    response_description="Evento removido com sucesso.",
    responses={404: {"description": "Não existe evento com esse identificador."}},
)
def delete_event(
    event_id: Annotated[int, Path(gt=0, description="Identificador do evento.")],
    service: Annotated[EventService, Depends(get_event_service)],
) -> Response:
    try:
        service.delete_event(event_id)
    except EventNotFoundError as error:
        raise not_found(error) from error
    return Response(status_code=204)
