# =============================================================================
# Makefile - Common development tasks for Production Agents course
# =============================================================================
# This Makefile provides easy shortcuts for common operations.
# If you're on Windows without make, use the scripts/ folder instead:
#   - PowerShell: .\scripts\setup.ps1
#   - Command Prompt: scripts\setup.bat
#
# Usage:
#   make setup     - First-time setup (create venv, install deps)
#   make run       - Run the first lesson
#   make verify    - Verify your setup is correct
#   make test      - Run all tests
#   make clean     - Remove generated files and venv
#
# Why make?
#   make is the universal "task runner" for developers. It's been around
#   since 1976 and is installed by default on macOS and Linux. It's the
#   lowest-common-denominator way to automate repetitive tasks.
# =============================================================================

# Use bash for shell commands (more consistent than sh)
SHELL := /bin/bash

# Detect Python command (python3 on macOS/Linux, python on Windows)
PYTHON := $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null)

# Virtual environment directory
VENV := .venv
VENV_BIN := $(VENV)/bin
VENV_PYTHON := $(VENV_BIN)/python
VENV_PIP := $(VENV_BIN)/pip

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

# Default target when you just run 'make'
.DEFAULT_GOAL := help

# =============================================================================
# SETUP & INSTALLATION
# =============================================================================

.PHONY: setup
setup: $(VENV_PYTHON) install env-check ## First-time setup (venv + deps + env check)
	@echo ""
	@echo -e "$(GREEN)Setup complete!$(NC)"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Activate the venv: source .venv/bin/activate"
	@echo "  2. Edit .env and add your API keys"
	@echo "  3. Run: make verify"
	@echo ""

$(VENV_PYTHON):
	@echo -e "$(BLUE)Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo -e "$(GREEN)Virtual environment created at $(VENV)/$(NC)"

.PHONY: install
install: $(VENV_PYTHON) ## Install all dependencies
	@echo -e "$(BLUE)Upgrading pip...$(NC)"
	$(VENV_PIP) install --upgrade pip --quiet
	@echo -e "$(BLUE)Installing dependencies...$(NC)"
	$(VENV_PIP) install -e . --quiet
	@echo -e "$(GREEN)Dependencies installed$(NC)"

.PHONY: install-dev
install-dev: $(VENV_PYTHON) ## Install with development dependencies
	@echo -e "$(BLUE)Installing with dev dependencies...$(NC)"
	$(VENV_PIP) install --upgrade pip --quiet
	$(VENV_PIP) install -e ".[dev]" --quiet
	@echo -e "$(GREEN)Dev dependencies installed$(NC)"

.PHONY: env-check
env-check: ## Check/create .env file
	@if [ ! -f .env ]; then \
		if [ -f .env.example ]; then \
			cp .env.example .env; \
			echo -e "$(YELLOW)Created .env from .env.example - edit it to add your API keys$(NC)"; \
		fi \
	else \
		echo -e "$(GREEN).env file exists$(NC)"; \
	fi

# =============================================================================
# RUNNING CODE
# =============================================================================

.PHONY: run
run: ## Run the first lesson (what is an agent?)
	$(VENV_PYTHON) -m segment_1_foundations.01_what_is_an_agent

.PHONY: verify
verify: ## Verify your setup is working
	$(VENV_PYTHON) -m scripts.verify_setup

.PHONY: cost
cost: ## Run the cost calculator
	$(VENV_PYTHON) -m scripts.cost_calculator

# Run any segment lesson: make lesson SEGMENT=1 LESSON=01
.PHONY: lesson
lesson: ## Run a specific lesson (usage: make lesson SEGMENT=1 LESSON=01)
	@if [ -z "$(SEGMENT)" ] || [ -z "$(LESSON)" ]; then \
		echo "Usage: make lesson SEGMENT=1 LESSON=01"; \
		echo ""; \
		echo "Available lessons:"; \
		ls -1 segment_*/[0-9]*.py 2>/dev/null | sed 's/\.py//' | sed 's/_/ - /' || echo "  (none found)"; \
	else \
		$(VENV_PYTHON) -m segment_$(SEGMENT)_*$(LESSON)* 2>/dev/null || \
		echo "Lesson not found. Check segment_$(SEGMENT)_* folder."; \
	fi

# =============================================================================
# TESTING & QUALITY
# =============================================================================

.PHONY: test
test: ## Run all tests
	$(VENV_PYTHON) -m pytest tests/ -v

.PHONY: test-cov
test-cov: ## Run tests with coverage report
	$(VENV_PYTHON) -m pytest tests/ --cov=. --cov-report=term-missing

.PHONY: lint
lint: ## Run linting (ruff)
	$(VENV_PYTHON) -m ruff check .

.PHONY: format
format: ## Format code (black + ruff)
	$(VENV_PYTHON) -m black .
	$(VENV_PYTHON) -m ruff check --fix .

.PHONY: typecheck
typecheck: ## Run type checking (mypy)
	$(VENV_PYTHON) -m mypy .

# =============================================================================
# CLEANUP
# =============================================================================

.PHONY: clean
clean: ## Remove build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

.PHONY: clean-all
clean-all: clean ## Remove venv and all generated files
	rm -rf $(VENV)
	@echo -e "$(YELLOW)Virtual environment removed. Run 'make setup' to recreate.$(NC)"

# =============================================================================
# HELP
# =============================================================================

.PHONY: help
help: ## Show this help message
	@echo ""
	@echo "Production Agents - Development Commands"
	@echo "========================================="
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Quick start:"
	@echo "  make setup   - Set up everything (run this first)"
	@echo "  make verify  - Check your installation"
	@echo "  make run     - Start the first lesson"
	@echo ""
