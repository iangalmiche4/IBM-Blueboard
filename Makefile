# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Project name
PROJECT_NAME := ibm-blueboard

# Container names
FRONTEND_CONTAINER := $(PROJECT_NAME)-frontend
BACKEND_CONTAINER := $(PROJECT_NAME)-backend
DB_CONTAINER := $(PROJECT_NAME)-database

help: ## Show this help message
	@echo "$(BLUE)IBM Blueboard - Makefile Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

setup: ## Setup Podman environment
	@echo "$(BLUE)Setting up Podman environment...$(NC)"
	@if [ ! -x /usr/bin/podman ] && [ ! -x /usr/local/bin/podman ]; then \
		echo "$(RED)Error: Podman is not installed$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Setup complete (WSL native check)!$(NC)"

start: setup ## Start all services (frontend, backend, database)
	@echo "$(BLUE)Starting IBM Blueboard...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Creating .env from .env.example...$(NC)"; \
		cp .env.example .env; \
	fi
	@podman compose up -d 2>&1 | grep -v "Executing external compose provider"
	@echo "$(GREEN)✓ All services started!$(NC)"
	@echo ""
	@echo "$(BLUE)Access URLs:$(NC)"
	@echo "  Frontend:  $(GREEN)http://localhost:3000$(NC)"
	@echo "  Backend:   $(GREEN)http://localhost:8000$(NC)"
	@echo "  API Docs:  $(GREEN)http://localhost:8000/docs$(NC)"
	@echo ""
	@echo "Run '$(YELLOW)make logs$(NC)' to view logs"
	@echo "Run '$(YELLOW)make generate-data$(NC)' to populate database"

stop: ## Stop all services
	@echo "$(BLUE)Stopping IBM Blueboard...$(NC)"
	@podman compose down 2>&1 | grep -v "Executing external compose provider"
	@echo "$(GREEN)✓ All services stopped$(NC)"

restart: ## Restart all services
	@echo "$(BLUE)Restarting all services...$(NC)"
	@$(MAKE) stop
	@$(MAKE) start

restart-frontend: ## Restart only frontend service
	@echo "$(BLUE)Restarting frontend...$(NC)"
	@podman compose restart frontend 2>&1 | grep -v "Executing external compose provider"
	@echo "$(GREEN)✓ Frontend restarted$(NC)"

restart-backend: ## Restart only backend service
	@echo "$(BLUE)Restarting backend...$(NC)"
	@podman compose restart backend 2>&1 | grep -v "Executing external compose provider"
	@echo "$(GREEN)✓ Backend restarted$(NC)"

restart-database: ## Restart only database service
	@echo "$(BLUE)Restarting database...$(NC)"
	@podman compose restart database 2>&1 | grep -v "Executing external compose provider"
	@echo "$(GREEN)✓ Database restarted$(NC)"

logs: ## Show logs from all services
	podman compose logs -f

logs-frontend: ## Show logs from frontend service
	podman compose logs -f frontend

logs-backend: ## Show logs from backend service
	podman compose logs -f backend

logs-database: ## Show logs from database service
	podman compose logs -f database

status: ## Show status of all services
	@echo "$(BLUE)IBM Blueboard Services Status:$(NC)"
	@echo ""
	@podman compose ps 2>&1 | grep -v "Executing external compose provider"

generate-data: ## Generate test data in database
	@echo "$(BLUE)Generating test data...$(NC)"
	@if ! podman ps | grep -q $(BACKEND_CONTAINER); then \
		echo "$(RED)Error: Backend container is not running$(NC)"; \
		echo "Run '$(YELLOW)make start$(NC)' first"; \
		exit 1; \
	fi
	podman exec $(BACKEND_CONTAINER) python scripts/generate_fake_data.py
	@echo "$(GREEN)✓ Test data generated successfully!$(NC)"

clear-data: ## Clear all data from database
	@echo "$(YELLOW)Warning: This will delete all data from the database!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(BLUE)Clearing database...$(NC)"; \
		if ! podman ps | grep -q $(DB_CONTAINER); then \
			echo "$(RED)Error: Database container is not running$(NC)"; \
			echo "Run '$(YELLOW)make start$(NC)' first"; \
			exit 1; \
		fi; \
		podman exec $(DB_CONTAINER) psql -U blueboard -d blueboard -c "TRUNCATE TABLE sales, customers, products, satisfaction, inventory, promotions, returns RESTART IDENTITY CASCADE;"; \
		echo "$(GREEN)✓ Database cleared successfully!$(NC)"; \
		echo "$(YELLOW)Run '$(YELLOW)make generate-data$(NC)' to populate with new data$(NC)"; \
	else \
		echo "$(YELLOW)Operation cancelled$(NC)"; \
	fi

clean: ## Stop services and remove containers, volumes, and networks
	@echo "$(YELLOW)Warning: This will remove all containers, volumes, and data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(BLUE)Cleaning up...$(NC)"; \
		podman compose down -v 2>&1 | grep -v "Executing external compose provider"; \
		echo "$(GREEN)✓ Cleanup complete$(NC)"; \
	else \
		echo "$(YELLOW)Cleanup cancelled$(NC)"; \
	fi

shell-frontend: ## Open shell in frontend container
	podman exec -it $(FRONTEND_CONTAINER) /bin/sh

shell-backend: ## Open shell in backend container
	podman exec -it $(BACKEND_CONTAINER) /bin/bash

shell-database: ## Open PostgreSQL shell
	podman exec -it $(DB_CONTAINER) psql -U blueboard -d blueboard

build: ## Rebuild all containers
	@echo "$(BLUE)Rebuilding containers...$(NC)"
	@podman compose build 2>&1 | grep -v "Executing external compose provider"
	@echo "$(GREEN)✓ Build complete$(NC)"

build-frontend: ## Rebuild frontend container
	@echo "$(BLUE)Rebuilding frontend...$(NC)"
	@podman compose build frontend 2>&1 | grep -v "Executing external compose provider"
	@echo "$(GREEN)✓ Frontend build complete$(NC)"

build-backend: ## Rebuild backend container
	@echo "$(BLUE)Rebuilding backend...$(NC)"
	@podman compose build backend 2>&1 | grep -v "Executing external compose provider"
	@echo "$(GREEN)✓ Backend build complete$(NC)"

dev: ## Start in development mode with logs
	@$(MAKE) start
	@$(MAKE) logs

test: ## Run backend tests
	@echo "$(BLUE)Running backend tests...$(NC)"
	@if ! podman ps | grep -q $(BACKEND_CONTAINER); then \
		echo "$(RED)Error: Backend container is not running$(NC)"; \
		echo "Run '$(YELLOW)make start$(NC)' first"; \
		exit 1; \
	fi
	podman exec $(BACKEND_CONTAINER) pytest
	@echo "$(GREEN)✓ Tests completed$(NC)"

test-verbose: ## Run backend tests with verbose output
	@echo "$(BLUE)Running backend tests (verbose)...$(NC)"
	@if ! podman ps | grep -q $(BACKEND_CONTAINER); then \
		echo "$(RED)Error: Backend container is not running$(NC)"; \
		echo "Run '$(YELLOW)make start$(NC)' first"; \
		exit 1; \
	fi
	podman exec $(BACKEND_CONTAINER) pytest -v
	@echo "$(GREEN)✓ Tests completed$(NC)"

test-coverage: ## Run backend tests with coverage report
	@echo "$(BLUE)Running backend tests with coverage...$(NC)"
	@if ! podman ps | grep -q $(BACKEND_CONTAINER); then \
		echo "$(RED)Error: Backend container is not running$(NC)"; \
		echo "Run '$(YELLOW)make start$(NC)' first"; \
		exit 1; \
	fi
	podman exec $(BACKEND_CONTAINER) pytest --cov=app --cov-report=term-missing
	@echo "$(GREEN)✓ Tests completed$(NC)"

organize-imports-frontend: ## Organize and fix imports in frontend
	@echo "$(BLUE)Organizing frontend imports...$(NC)"
	cd frontend && npm run organize-imports
	@echo "$(GREEN)✓ Frontend imports organized$(NC)"

organize-imports-backend: ## Organize and fix imports in backend
	@echo "$(BLUE)Organizing backend imports...$(NC)"
	cd backend && python3 -m autoflake --remove-all-unused-imports --in-place --recursive app/ tests/
	cd backend && python3 -m isort app/ tests/
	@echo "$(GREEN)✓ Backend imports organized$(NC)"

organize-imports: ## Organize imports in both frontend and backend
	@$(MAKE) organize-imports-frontend
	@$(MAKE) organize-imports-backend
	@echo "$(GREEN)✓ All imports organized!$(NC)"

format-frontend: ## Format frontend code with Prettier
	@echo "$(BLUE)Formatting frontend code...$(NC)"
	cd frontend && npx prettier --write "src/**/*.{js,jsx,ts,tsx,json,css,scss,md}"
	@echo "$(GREEN)✓ Frontend code formatted$(NC)"

format-config: ## Format config files (docker-compose, Markdown)
	@echo "$(BLUE)Formatting config files...$(NC)"
	npx prettier --write "**/*.{md,yml,yaml}"
	@echo "$(GREEN)✓ Config files formatted$(NC)"
	@echo "$(YELLOW)Note: Dockerfiles are not auto-formatted (no standard formatter available)$(NC)"

format-backend: ## Format backend code with Black
	@echo "$(BLUE)Formatting backend code...$(NC)"
	cd backend && python3 -m black app/ tests/
	@echo "$(GREEN)✓ Backend code formatted$(NC)"

format-database: ## Format database SQL files with pg_format
	@echo "$(BLUE)Formatting database SQL files...$(NC)"
	@if command -v pg_format >/dev/null 2>&1; then \
		find database -name "*.sql" -type f -exec pg_format -i {} \; && \
		echo "$(GREEN)✓ Database SQL files formatted$(NC)"; \
	else \
		echo "$(YELLOW)⚠ pg_format not installed. Install with: brew install pgformatter (macOS) or apt install pgformatter (Linux)$(NC)"; \
	fi

format: ## Format all code (frontend, backend, database, config)
	@$(MAKE) format-frontend
	@$(MAKE) format-backend
	@$(MAKE) format-database
	@$(MAKE) format-config
	@echo "$(GREEN)✓ All code formatted!$(NC)"

ps: status ## Alias for status

# Default target
# Phony targets
.PHONY: help setup start stop restart restart-frontend restart-backend restart-database \
	       logs logs-frontend logs-backend logs-database status generate-data clear-data clean \
	       shell-frontend shell-backend shell-database build build-frontend build-backend \
	       dev test test-verbose test-coverage organize-imports-frontend organize-imports-backend \
	       organize-imports format-frontend format-backend format-database format-config format ps
.DEFAULT_GOAL := help