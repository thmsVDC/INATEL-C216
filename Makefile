.PHONY: help install test lint format run clean

BACKEND_DIR := backend
PYTHON := poetry run python
PYTEST := poetry run pytest
UVICORN := poetry run uvicorn
RUFF := poetry run ruff

help:
	@echo "Comandos disponiveis:"
	@echo "  install - Instalar dependencias"
	@echo "  test - Executar testes"
	@echo "  lint - Executar linter"
	@echo "  format - Formatar codigo"
	@echo "  run - Executar servidor"
	@echo "  clean - Limpar artefatos"

install:
	cd $(BACKEND_DIR) && poetry install

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