from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_flag_provider
from app.schemas.game import FlagQuizQuestion
from app.services.flag_provider import FlagProvider, FlagProviderError

router = APIRouter(prefix="/flags", tags=["flags"])


@router.get("/quiz", response_model=list[FlagQuizQuestion])
async def get_quiz_questions(
    provider: Annotated[FlagProvider, Depends(get_flag_provider)],
    count: Annotated[int, Query(ge=1, le=20)] = 10,
) -> list[FlagQuizQuestion]:
    try:
        return await provider.get_quiz_questions(count)
    except FlagProviderError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
