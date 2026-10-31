# INATEL C216 — Jogo de bandeiras

Projeto acadêmico de Sistemas Distribuídos com uma interface web, uma API e um banco PostgreSQL. O ambiente completo pode ser iniciado com Docker Compose.

## O que roda

- **Frontend:** React e Vite, servido por Nginx.
- **Backend:** API FastAPI com SQLAlchemy e migrações Alembic; busca países e bandeiras na [REST Countries](https://restcountries.com/docs/countries).
- **Banco:** PostgreSQL com volume persistente.

## Executar o projeto

Você só precisa do Docker Desktop com Docker Compose, do Make instalado e de uma chave gratuita da REST Countries.

1. Crie uma chave gratuita em [restcountries.com](https://restcountries.com/sign-up).
2. Na pasta raiz do projeto, copie o arquivo de exemplo:

   ```bash
   copy .env.example .env
   ```

3. Abra o arquivo `.env` e substitua `cole_sua_chave_aqui` pela chave criada.
4. Construa as imagens e inicie os serviços:

   ```bash
   make docker-up
   ```

5. Confira se os serviços estão ativos:

   ```bash
   docker compose ps
   ```

4. Acesse:

   - Frontend: http://localhost:5173
   - Documentação da API: http://localhost:8000/docs
   - PostgreSQL: localhost:5432

O backend aplica as migrações automaticamente ao iniciar. Ele consulta a REST Countries pela chave configurada e mantém a lista de países em cache por uma hora. A chave fica no backend e não é enviada ao navegador.

## Parar os serviços

```bash
make docker-down
```

Os dados do PostgreSQL permanecem no volume postgres_data quando os containers são parados.

## Estrutura

```text
.
├── .github/workflows/     # CI do backend e do frontend
├── .env.example           # Configuração da chave da REST Countries
├── backend/
│   ├── app/
│   │   ├── api/routes/    # Endpoints FastAPI, incluindo o quiz de bandeiras
│   │   ├── repositories/  # Acesso ao banco
│   │   ├── schemas/       # Schemas Pydantic
│   │   ├── services/      # Regras do jogo
│   │   ├── database.py    # Conexão SQLAlchemy
│   │   └── models.py      # Modelos ORM
│   ├── migrations/        # Migrações Alembic
│   └── tests/             # Testes do backend
├── frontend/
│   ├── e2e/               # Testes Playwright
│   └── src/
│       ├── api/           # Comunicação com o backend
│       ├── components/    # Componentes React
│       └── App.jsx        # Quiz com perguntas obtidas pela API
├── docker-compose.yml
└── Makefile
```
