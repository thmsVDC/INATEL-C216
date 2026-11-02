# OrganizaJá

O OrganizaJá é uma aplicação web para organizar eventos acadêmicos. A proposta é
reunir em um só lugar a divulgação de eventos, o controle de vagas e o
acompanhamento das inscrições.

## Funcionalidades planejadas

- Cadastro, consulta, edição e exclusão de eventos.
- Busca e filtros por nome, categoria e período.
- Inscrição e cancelamento de participantes.
- Controle de capacidade, vagas disponíveis e lista de inscritos.
- Validação para evitar inscrições duplicadas e eventos lotados.

## Tecnologias

- **Frontend:** React e JavaScript.
- **Backend:** Python, FastAPI e Poetry para gerenciar as dependências.
- **Banco de dados:** PostgreSQL, SQLAlchemy e Alembic.
- **Execução:** Docker Compose e Makefile para os comandos de desenvolvimento e manutenção.
- **Qualidade:** Pytest, Vitest, Testing Library, Playwright, Ruff, Biome e GitHub Actions.

## Arquitetura prevista

O frontend consumirá a API REST do backend. O backend aplicará as regras de
negócio e persistirá eventos e inscrições no PostgreSQL. O Docker Compose será
usado para executar os serviços em conjunto.

## Estado do projeto

O projeto está em desenvolvimento. As instruções de configuração, execução,
migrações e testes serão adicionadas conforme esses recursos forem
implementados e validados.

O `pyproject.toml` do backend terá uma descrição compatível com o que a API
realmente faz: “API para gestão de eventos acadêmicos, inscrições de
participantes e controle de vagas.”
