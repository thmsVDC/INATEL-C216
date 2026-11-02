from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from sqlalchemy.orm import Session

from app.api.dependencies import get_flag_provider
from app.database import get_db
from app.repositories.game_repository import GameRepository
from app.schemas.game import (
    FlagQuestion,
    GamePatch,
    GameReplace,
    GameResponse,
    GuessRequest,
    GuessResponse,
)
from app.services.flag_provider import (
    FlagProvider,
    FlagProviderError,
)
from app.services.game_service import GameNotFoundError, GameService

router = APIRouter(prefix="/games", tags=["games"])


def get_game_service(session: Session = Depends(get_db)) -> GameService:
    return GameService(GameRepository(session))


def to_game_response(game, choices: list[str] | None = None) -> GameResponse:
    return GameResponse(
        id=game.id,
        flag_url=game.flag_url,
        score=game.score,
        streak=game.streak,
        is_active=game.is_active,
        choices=choices or [],
    )


def not_found(error: GameNotFoundError) -> HTTPException:
    return HTTPException(status_code=404, detail=str(error))


@router.get("", response_model=list[GameResponse])
def list_games(
    limit: int = Query(default=50, ge=1, le=100),
    service: GameService = Depends(get_game_service),
) -> list[GameResponse]:
    return [to_game_response(game) for game in service.list_games(limit)]


@router.get("/{game_id}", response_model=GameResponse)
def get_game(
    game_id: int = Path(gt=0),
    service: GameService = Depends(get_game_service),
) -> GameResponse:
    try:
        return to_game_response(service.get_game(game_id))
    except GameNotFoundError as error:
        raise not_found(error) from error


@router.post("", response_model=GameResponse, status_code=201)
async def create_game(
    service: GameService = Depends(get_game_service),
    provider: FlagProvider = Depends(get_flag_provider),
) -> GameResponse:
    try:
        questions = await provider.get_quiz_questions(1)
        question = questions[0]
        game = service.create_game(
            FlagQuestion(correct_country=question.country, flag_url=question.flag_url)
        )
        return to_game_response(game, question.choices)
    except FlagProviderError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@router.put("/{game_id}", response_model=GameResponse)
def replace_game(
    data: GameReplace,
    game_id: int = Path(gt=0),
    service: GameService = Depends(get_game_service),
) -> GameResponse:
    try:
        game = service.replace_game(game_id, data)
        return to_game_response(game)
    except GameNotFoundError as error:
        raise not_found(error) from error


@router.patch("/{game_id}", response_model=GameResponse)
def patch_game(
    data: GamePatch,
    game_id: int = Path(gt=0),
    service: GameService = Depends(get_game_service),
) -> GameResponse:
    try:
        game = service.patch_game(game_id, data)
        return to_game_response(game)
    except GameNotFoundError as error:
        raise not_found(error) from error


@router.post("/{game_id}/guess", response_model=GuessResponse)
async def submit_guess(
    data: GuessRequest,
    game_id: int = Path(gt=0),
    service: GameService = Depends(get_game_service),
    provider: FlagProvider = Depends(get_flag_provider),
) -> GuessResponse:
    try:
        service.get_game(game_id)

        next_question = None
        choices: list[str] = []
        if not data.finish:
            questions = await provider.get_quiz_questions(1)
            quiz_question = questions[0]
            next_question = FlagQuestion(
                correct_country=quiz_question.country,
                flag_url=quiz_question.flag_url,
            )
            choices = quiz_question.choices

        game, is_correct, correct_country = service.submit_guess(
            game_id,
            data.answer,
            next_question,
            data.finish,
        )

        return GuessResponse(
            is_correct=is_correct,
            correct_country=correct_country,
            game=to_game_response(game, choices),
        )
    except GameNotFoundError as error:
        raise not_found(error) from error
    except FlagProviderError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@router.delete("/{game_id}", status_code=204)
def delete_game(
    game_id: int = Path(gt=0),
    service: GameService = Depends(get_game_service),
) -> Response:
    try:
        service.delete_game(game_id)
    except GameNotFoundError as error:
        raise not_found(error) from error

    return Response(status_code=204)
