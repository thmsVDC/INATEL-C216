from pydantic import BaseModel, Field


class FlagCreate(BaseModel):
    country: str = Field(min_length=1)
    country_code: str = Field(min_length=2, max_length=2)
    flag_url: str = Field(min_length=1)


class FlagPatch(BaseModel):
    country: str | None = Field(default=None, min_length=1)
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    flag_url: str | None = Field(default=None, min_length=1)


class Flag(FlagCreate):
    id: int