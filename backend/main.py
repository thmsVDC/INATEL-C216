from fastapi import FastAPI

from app.api.routes.flags import router as flags_router

app = FastAPI()
app.include_router(flags_router, prefix="/api/v1")