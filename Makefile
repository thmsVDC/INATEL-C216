.PHONY: help install backend-install frontend-install test lint format run front-dev front-build

BACKEND_DIR := backend
FRONTEND_DIR := frontend

help:
	@echo "Comandos do OrganizaJa:"
	@echo "  install          - Instala as dependencias do backend e frontend"
	@echo "  backend-install  - Instala as dependencias Python pelo Poetry"
	@echo "  frontend-install - Instala as dependencias JavaScript"
	@echo "  test             - Executa os testes automatizados"
	@echo "  lint             - Verifica o estilo do backend e frontend"
	@echo "  format           - Formata o codigo Python"
	@echo "  run              - Inicia a API FastAPI"
	@echo "  front-dev        - Inicia o frontend Vite"
	@echo "  front-build      - Gera o build de producao do frontend"

install: backend-install frontend-install

backend-install:
	cd $(BACKEND_DIR) && poetry install --no-root

frontend-install:
	npm --prefix $(FRONTEND_DIR) install

test:
	cd $(BACKEND_DIR) && poetry run pytest
	npm --prefix $(FRONTEND_DIR) run test

lint:
	cd $(BACKEND_DIR) && poetry run ruff check .
	npm --prefix $(FRONTEND_DIR) run lint

format:
	cd $(BACKEND_DIR) && poetry run ruff format .

run:
	cd $(BACKEND_DIR) && poetry run uvicorn main:app --reload

front-dev:
	npm --prefix $(FRONTEND_DIR) run dev

front-build:
	npm --prefix $(FRONTEND_DIR) run build
