# OrganizaJá

Uma aplicação para criar eventos acadêmicos, divulgar informações e gerenciar inscrições e vagas em um só lugar.

## O que você pode fazer

- Criar, consultar, editar e excluir eventos.
- Buscar eventos por título, categoria e período.
- Inscrever participantes e cancelar inscrições.
- Acompanhar a lista de inscritos e as vagas disponíveis.
- Evitar inscrições duplicadas e respeitar a capacidade de cada evento.

## Executar com Docker

### Pré-requisitos

- Docker Desktop instalado e em execução, com Docker Compose disponível.
- `make` instalado.

### Iniciar

Na pasta do projeto, execute:

```bash
make docker-up
```

Esse comando constrói as imagens e inicia o frontend, a API e o PostgreSQL. O backend aplica as migrations do banco ao iniciar.

Quando os serviços estiverem prontos, acesse:

- **Aplicação:** http://localhost:5173
- **Documentação da API:** http://localhost:8000/docs
- **Verificação da API:** http://localhost:8000/health

### Comandos úteis

```bash
make docker-logs  # acompanha os logs dos serviços
make docker-down  # encerra os serviços
make test         # executa os testes da API e do frontend
make lint         # verifica o código Python e JavaScript
```

Para executar o teste de ponta a ponta no navegador, com a aplicação e o PostgreSQL em Docker:

```bash
make docker-up
make e2e-install
make e2e
```

O teste cria um evento, faz uma inscrição, recarrega a página para confirmar que ela foi persistida e cancela a inscrição.

## API

Os endpoints estão disponíveis sob `/api/v1` e a documentação interativa fica em `/docs`.

| Método | Endpoint | Ação |
| --- | --- | --- |
| `GET` | `/api/v1/events` | Lista e filtra eventos |
| `POST` | `/api/v1/events` | Cria um evento |
| `GET` | `/api/v1/events/{id}` | Consulta um evento |
| `PUT` | `/api/v1/events/{id}` | Atualiza um evento |
| `DELETE` | `/api/v1/events/{id}` | Exclui um evento e suas inscrições |
| `GET` | `/api/v1/events/{id}/registrations` | Lista participantes inscritos |
| `POST` | `/api/v1/events/{id}/registrations` | Inscreve um participante |
| `DELETE` | `/api/v1/events/{id}/registrations/{registration_id}` | Cancela uma inscrição |

## Estrutura do projeto

```text
.
├── .github/workflows/ci.yml  # testes e verificações no GitHub Actions
├── backend/
│   ├── app/
│   │   ├── api/routes/       # endpoints FastAPI
│   │   ├── repositories/     # acesso ao PostgreSQL
│   │   ├── schemas/          # validação e respostas da API
│   │   ├── services/         # regras de negócio
│   │   └── models.py         # modelos SQLAlchemy
│   ├── migrations/           # histórico Alembic
│   └── tests/                # testes da API
├── frontend/
│   ├── src/
│   │   ├── api/              # comunicação com o backend e testes
│   │   ├── App.jsx           # interface do OrganizaJá
│   │   └── style.css         # estilos
│   ├── e2e/                  # cenários Playwright com a aplicação em execução
│   └── playwright.config.js
├── docker-compose.yml
└── Makefile
```

## Tecnologias

React, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Poetry, Docker Compose, Pytest, Vitest, Playwright, Ruff, Biome e GitHub Actions.
