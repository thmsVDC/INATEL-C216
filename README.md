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

## Frontend moderno

O frontend do jogo de bandeiras usa JavaScript, React, Vite e Tailwind CSS. Nesta prática, a interface trabalha com dados locais de demonstração; a integração com o backend e a persistência ficam para a próxima prática.

Com Node.js 22.12 ou superior, instale as dependências e inicie o servidor de desenvolvimento:

    make front-install
    make front-dev

Para executar os testes de navegador pela primeira vez, instale o Chromium do Playwright:

    make front-e2e-install

Os principais comandos ficam disponíveis pelo Makefile:

    make front-build
    make front-test
    make front-test-e2e
    make front-lint
    make front-format
    make front-format-check
    make front-check

Biome executa lint, formatação e organização de imports. Vitest e React Testing Library cobrem os componentes e interações; Playwright verifica o fluxo completo no Chromium. A workflow Frontend CI roda o lint primeiro e, em seguida, testes, formatação e build.
