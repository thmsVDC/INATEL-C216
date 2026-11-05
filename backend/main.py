from fastapi import FastAPI

from app.api.routes.events import router as events_router

app = FastAPI(
    title="OrganizaJá API",
    description=(
        "API para gestão de eventos acadêmicos, inscrições de participantes "
        "e controle de vagas."
    ),
    version="0.1.0",
)
app.include_router(events_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
