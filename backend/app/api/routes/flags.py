from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response

from app.schemas.flag import Flag, FlagCreate, FlagPatch
from app.services.flag_service import FlagNotFoundError, FlagService


router = APIRouter(prefix="/flags", tags=["flags"])

_flag_service = FlagService()


def get_flag_service() -> FlagService:
    return _flag_service


def _not_found(error: FlagNotFoundError) -> HTTPException:
    return HTTPException(status_code=404, detail=str(error))


@router.get("", response_model=list[Flag])
def list_flags(
    limit: int = Query(default=50, ge=1, le=100),
    service: FlagService = Depends(get_flag_service),
) -> list[Flag]:
    return service.list_flags(limit)


@router.get("/{flag_id}", response_model=Flag)
def get_flag(
    flag_id: int = Path(gt=0),
    service: FlagService = Depends(get_flag_service),
) -> Flag:
    try:
        return service.get_flag(flag_id)
    except FlagNotFoundError as error:
        raise _not_found(error) from error


@router.post("", response_model=Flag, status_code=201)
def create_flag(
    data: FlagCreate,
    service: FlagService = Depends(get_flag_service),
) -> Flag:
    return service.create_flag(data)


@router.put("/{flag_id}", response_model=Flag)
def replace_flag(
    data: FlagCreate,
    flag_id: int = Path(gt=0),
    service: FlagService = Depends(get_flag_service),
) -> Flag:
    try:
        return service.replace_flag(flag_id, data)
    except FlagNotFoundError as error:
        raise _not_found(error) from error


@router.patch("/{flag_id}", response_model=Flag)
def patch_flag(
    data: FlagPatch,
    flag_id: int = Path(gt=0),
    service: FlagService = Depends(get_flag_service),
) -> Flag:
    try:
        return service.patch_flag(flag_id, data)
    except FlagNotFoundError as error:
        raise _not_found(error) from error


@router.delete("/{flag_id}", status_code=204)
def delete_flag(
    flag_id: int = Path(gt=0),
    service: FlagService = Depends(get_flag_service),
) -> Response:
    try:
        service.delete_flag(flag_id)
    except FlagNotFoundError as error:
        raise _not_found(error) from error
    return Response(status_code=204)