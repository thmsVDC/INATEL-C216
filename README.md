# Práticas de Sistemas Distribuídos

## Testes do backend

Com Poetry instalado, execute a partir da raiz do repositório:

```bash
make install
make test
make lint
```

## Executar a aplicação com PostgreSQL

O Docker Compose inicia o PostgreSQL e configura `DATABASE_URL` no backend. Na primeira inicialização, o backend aplica as migrações do Alembic antes de iniciar a API:

```bash
make docker-up
```

Os dados do PostgreSQL ficam no volume `postgres_data` e continuam disponíveis depois de reiniciar os containers. Para parar e iniciar novamente:

```bash
make docker-down
make docker-up
```

Para usar outra conexão, defina `DATABASE_URL` no ambiente antes de executar o Compose. As migrações também podem ser aplicadas manualmente dentro de `backend` com `poetry run alembic upgrade head`.
