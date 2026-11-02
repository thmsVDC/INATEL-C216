from fastapi import FastAPI

app = FastAPI(
    title="OrganizaJá API",
    description=(
        "API para gestão de eventos acadêmicos, inscrições de participantes "
        "e controle de vagas."
    ),
    version="0.1.0",
)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
