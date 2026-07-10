PYTHON ?= python
BACKEND_DIR := backend
TEST_DIR := tests

.PHONY: help install format format-check lint lint-fix typecheck test check pre-commit-install pre-commit-run

help:
	@echo "Available targets:"
	@echo "  install"
	@echo "  format"
	@echo "  format-check"
	@echo "  lint"
	@echo "  lint-fix"
	@echo "  typecheck"
	@echo "  test"
	@echo "  check"
	@echo "  pre-commit-install"
	@echo "  pre-commit-run"

install:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e ".[dev]"

format:
	isort $(BACKEND_DIR) $(TEST_DIR)
	black $(BACKEND_DIR) $(TEST_DIR)

format-check:
	isort --check-only --diff $(BACKEND_DIR) $(TEST_DIR)
	black --check $(BACKEND_DIR) $(TEST_DIR)

lint:
	ruff check $(BACKEND_DIR) $(TEST_DIR)

lint-fix:
	ruff check --fix $(BACKEND_DIR) $(TEST_DIR)

typecheck:
	mypy $(BACKEND_DIR) $(TEST_DIR)

test:
	pytest

check: format-check lint typecheck test

pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files
