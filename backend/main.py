from fastapi import FastAPI

from app.api.routes.flags import router as flags_router
from app.api.routes.games import router as games_router

app = FastAPI()
app.include_router(games_router, prefix="/api/v1")
app.include_router(flags_router, prefix="/api/v1")
