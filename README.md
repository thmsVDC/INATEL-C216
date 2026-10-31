# INATEL C216 | Jogo de bandeiras

Um projeto de aprendizado de Sistemas Distribuídos: uma API para partidas do jogo de bandeiras e uma interface web para testar seus conhecimentos.

## O que tem aqui

- **Backend:** FastAPI, SQLAlchemy e PostgreSQL, com CRUD de partidas, palpites e migrações Alembic.
- **Frontend:** React, Vite e Tailwind CSS; quiz de dez bandeiras com pontuação, sequência de acertos e resultado final.
- **Qualidade:** testes automatizados, Biome, Ruff e GitHub Actions.

Nesta prática, o frontend usa dados locais. A integração com a API e a execução do frontend em containers ficam para a próxima etapa.

## Pré-requisitos

- Python 3.12 e Poetry
- Node.js 22.12 ou superior e npm
- Docker Desktop e Docker Compose

## Executar em desenvolvimento local

O PostgreSQL fica no Docker e o backend e o frontend rodam localmente.

Instale o backend e inicie o banco:

```bash
make install
docker compose up -d db
```

Aplique a migração e inicie a API em um terminal:

```bash
cd backend
poetry run alembic upgrade head
poetry run uvicorn main:app --reload
```

Em outro terminal, instale e inicie o frontend:

```bash
make front-install
make front-dev
```

Abra o frontend em http://localhost:5173 e a documentação da API em http://localhost:8000/docs.

## Executar API e PostgreSQL com Docker

Na raiz do projeto:

```bash
make docker-up
```

O Compose inicia o PostgreSQL e a API. A migração é aplicada automaticamente quando o backend sobe. A API fica em http://localhost:8000 e a documentação interativa em http://localhost:8000/docs.

Para usar também o frontend, deixe os containers em execução e inicie-o localmente:

```bash
make front-install
make front-dev
```

Para parar os serviços:

```bash
make docker-down
```

O banco usa o volume persistente postgres_data.

## Testes e qualidade

```bash
make test
make lint
make front-test
make front-test-e2e
make front-check
make front-build
```

Na primeira execução dos testes de navegador, instale o Chromium do Playwright:

```bash
make front-e2e-install
```

## Estrutura do projeto

```text
.
├── .github/workflows/     # CI do backend e do frontend
├── backend/
│   ├── app/
│   │   ├── api/routes/    # Endpoints da API
│   │   ├── repositories/  # Acesso aos dados
│   │   ├── schemas/       # Contratos Pydantic
│   │   ├── services/      # Regras do jogo
│   │   ├── database.py    # Conexão e sessões SQLAlchemy
│   │   └── models.py      # Modelos ORM
│   ├── migrations/        # Migrações Alembic
│   ├── tests/             # Testes unitários e de integração
│   └── main.py            # Inicialização FastAPI
├── frontend/
│   ├── e2e/               # Testes Playwright
│   ├── public/flags/      # Bandeiras SVG locais
│   └── src/
│       ├── components/    # Componentes React
│       ├── data/          # Perguntas e alternativas
│       └── test/          # Configuração de testes
├── docker-compose.yml
└── Makefile
```
