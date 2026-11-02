from pydantic import BaseModel, Field


class FlagQuestion(BaseModel):
    correct_country: str
    flag_url: str


class FlagQuizQuestion(BaseModel):
    country: str
    flag_url: str
    choices: list[str] = Field(min_length=4, max_length=4)


class GameState(BaseModel):
    id: int
    correct_country: str
    flag_url: str
    score: int = Field(default=0, ge=0)
    streak: int = Field(default=0, ge=0)
    is_active: bool = True


class GameResponse(BaseModel):
    id: int
    flag_url: str
    score: int
    streak: int
    is_active: bool
    choices: list[str] = Field(default_factory=list)


class GameReplace(BaseModel):
    correct_country: str = Field(min_length=1)
    flag_url: str = Field(min_length=1)
    score: int = Field(ge=0)
    streak: int = Field(ge=0)
    is_active: bool


class GamePatch(BaseModel):
    correct_country: str | None = Field(default=None, min_length=1)
    flag_url: str | None = Field(default=None, min_length=1)
    score: int | None = Field(default=None, ge=0)
    streak: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class GuessRequest(BaseModel):
    answer: str = Field(min_length=1)
    finish: bool = False


class GuessResponse(BaseModel):
    is_correct: bool
    correct_country: str | None = None
    game: GameResponse
