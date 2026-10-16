.PHONY: help install test lint format run clean docker-build docker-up docker-down docker-logs docker-restart docker-clean

BACKEND_DIR := backend
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
	@echo "  docker-up      - Sobe os containers em background"
	@echo "  docker-down    - Para e remove os containers"
	@echo "  docker-logs    - Exibe os logs dos containers"
	@echo "  docker-restart - Reinicia os containers"
	@echo "  docker-clean   - Remove containers, volumes e imagens"

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
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-restart:
	docker compose restart

docker-clean:
	docker compose down -v --rmi all