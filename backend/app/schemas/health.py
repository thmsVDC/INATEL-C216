from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok"] = Field(
        description="Indica que a API está respondendo normalmente."
    )
