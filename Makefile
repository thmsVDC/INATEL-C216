.PHONY: help install test lint format run clean docker-build docker-up docker-down docker-logs docker-restart docker-clean front-install front-dev front-build front-preview front-test front-test-e2e front-e2e-install front-lint front-format front-format-check front-check

BACKEND_DIR := backend
FRONTEND_DIR := frontend
PYTHON := poetry run python
PYTEST := poetry run pytest
UVICORN := poetry run uvicorn
RUFF := poetry run ruff

help:
	@echo "Comandos disponiveis:"
	@echo "  install        - Instalar dependencias"
	@echo "  test           - Executar testes"
	@echo "  lint           - Executar linter"
	@echo "  format         - Formatar codigo"
	@echo "  run            - Executar servidor"
	@echo "  clean          - Limpar artefatos"
	@echo "  docker-build   - Constroi as imagens Docker"
	@echo "  docker-up      - Constroi as imagens e sobe os containers em background"
	@echo "  docker-down    - Para e remove os containers"
	@echo "  docker-logs    - Exibe os logs dos containers"
	@echo "  docker-restart - Reinicia os containers"
	@echo "  docker-clean   - Remove containers, volumes e imagens"
	@echo "  front-install  - Instala as dependencias do frontend"
	@echo "  front-dev      - Inicia o frontend em desenvolvimento"
	@echo "  front-build    - Gera o build de producao do frontend"
	@echo "  front-preview  - Visualiza o build de producao"
	@echo "  front-test     - Executa os testes unitarios do frontend"
	@echo "  front-test-e2e - Executa os testes E2E do frontend"
	@echo "  front-e2e-install - Instala o Chromium do Playwright"
	@echo "  front-lint     - Verifica o lint do frontend"
	@echo "  front-format   - Formata o frontend"
	@echo "  front-format-check - Verifica a formatacao do frontend"
	@echo "  front-check    - Executa as verificacoes do Biome"

install:
	cd $(BACKEND_DIR) && poetry install --no-root

test:
	cd $(BACKEND_DIR) && $(PYTEST)

lint:
	cd $(BACKEND_DIR) && $(RUFF) check .

format:
	cd $(BACKEND_DIR) && $(RUFF) format .

run:
	cd $(BACKEND_DIR) && $(UVICORN) main:app --reload

clean:
	cd $(BACKEND_DIR) && rm -rf __pycache__ .pytest_cache .ruff_cache

docker-build:
	docker compose build

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-restart:
	docker compose restart

docker-clean:
	docker compose down -v --rmi all

front-install:
	npm --prefix $(FRONTEND_DIR) install

front-dev:
	npm --prefix $(FRONTEND_DIR) run dev

front-build:
	npm --prefix $(FRONTEND_DIR) run build

front-preview:
	npm --prefix $(FRONTEND_DIR) run preview

front-test:
	npm --prefix $(FRONTEND_DIR) run test

front-test-e2e:
	npm --prefix $(FRONTEND_DIR) run test:e2e

front-e2e-install:
	cd $(FRONTEND_DIR) && npx playwright install chromium

front-lint:
	npm --prefix $(FRONTEND_DIR) run lint

front-format:
	npm --prefix $(FRONTEND_DIR) run format

front-format-check:
	npm --prefix $(FRONTEND_DIR) run format:check

front-check:
	npm --prefix $(FRONTEND_DIR) run check
