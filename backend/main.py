from fastapi import FastAPI

from app.api.routes.events import router as events_router
from app.api.routes.registrations import router as registrations_router
from app.schemas.health import HealthResponse

app = FastAPI(
    title="OrganizaJá API",
    summary="API para organizar eventos acadêmicos e inscrições.",
    description=(
        "## Sobre a API\n\n"
        "O OrganizaJá ajuda a comunidade acadêmica a divulgar eventos, "
        "controlar vagas e acompanhar inscrições.\n\n"
        "### Recursos\n"
        "- **Eventos:** cadastro, consulta, edição, exclusão e filtros.\n"
        "- **Inscrições:** listagem, inscrição e cancelamento, com controle "
        "de duplicidade e lotação.\n"
        "- **Saúde:** verificação de disponibilidade da API.\n\n"
        "As datas devem ser enviadas no formato ISO 8601 com fuso horário."
    ),
    version="0.1.0",
    openapi_tags=[
        {
            "name": "events",
            "description": (
                "**Eventos:** consulte, filtre e gerencie os eventos acadêmicos."
            ),
        },
        {
            "name": "registrations",
            "description": (
                "**Inscrições:** acompanhe participantes e controle as vagas "
                "dos eventos."
            ),
        },
        {
            "name": "health",
            "description": "**Saúde:** verifique se a API está disponível.",
        },
    ],
)
app.include_router(events_router, prefix="/api/v1")
app.include_router(registrations_router, prefix="/api/v1")


@app.get(
    "/health",
    tags=["health"],
    response_model=HealthResponse,
    summary="Verificar disponibilidade da API",
    description="Retorna o estado básico da API para verificações de disponibilidade.",
    response_description="Estado atual da API.",
)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")
