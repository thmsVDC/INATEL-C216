from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.services.event_service import EventNotFoundError, EventService

router = APIRouter(prefix="/events", tags=["events"])


def get_event_service(
    session: Annotated[Session, Depends(get_db)],
) -> EventService:
    return EventService(EventRepository(session))


def not_found(error: EventNotFoundError) -> HTTPException:
    return HTTPException(status_code=404, detail=str(error))


@router.get("", response_model=list[EventResponse])
def list_events(
    service: Annotated[EventService, Depends(get_event_service)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Sequence[EventResponse]:
    return service.list_events(limit, offset)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: Annotated[int, Path(gt=0)],
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventResponse:
    try:
        return service.get_event(event_id)
    except EventNotFoundError as error:
        raise not_found(error) from error


@router.post("", response_model=EventResponse, status_code=201)
def create_event(
    data: EventCreate,
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventResponse:
    return service.create_event(data)


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    data: EventUpdate,
    event_id: Annotated[int, Path(gt=0)],
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventResponse:
    try:
        return service.update_event(event_id, data)
    except EventNotFoundError as error:
        raise not_found(error) from error


@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: Annotated[int, Path(gt=0)],
    service: Annotated[EventService, Depends(get_event_service)],
) -> Response:
    try:
        service.delete_event(event_id)
    except EventNotFoundError as error:
        raise not_found(error) from error
    return Response(status_code=204)
