.PHONY: help install dev test lint format clean build up down logs shell

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install dependencies
	pip install -r requirements.txt
	cd frontend && npm install

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -e ".[dev]"
	cd frontend && npm install

# Development
dev: ## Start development environment
	docker-compose up -d postgres redis
	cd backend/inventory-service && uvicorn main:app --reload --port 8001 &
	cd backend/crm-service && uvicorn main:app --reload --port 8002 &
	cd backend/user-service && uvicorn main:app --reload --port 8003 &
	cd backend/notification-service && uvicorn main:app --reload --port 8004 &
	cd frontend && npm run dev

dev-full: ## Start full development environment with all services
	docker-compose up -d

# Testing
test: ## Run all tests
	pytest backend/ --cov=backend --cov-report=html --cov-report=term-missing
	cd frontend && npm test

test-unit: ## Run unit tests only
	pytest backend/ -m "not integration" --cov=backend

test-integration: ## Run integration tests
	pytest backend/ -m integration

test-frontend: ## Run frontend tests
	cd frontend && npm test

# Code Quality
lint: ## Run linting
	flake8 backend/
	cd frontend && npm run lint

format: ## Format code
	black backend/
	isort backend/
	cd frontend && npm run format

format-check: ## Check code formatting
	black --check backend/
	isort --check-only backend/
	cd frontend && npm run format:check

type-check: ## Run type checking
	mypy backend/
	cd frontend && npm run type-check

# Database
db-migrate: ## Run database migrations
	cd backend/inventory-service && alembic upgrade head
	cd backend/crm-service && alembic upgrade head
	cd backend/user-service && alembic upgrade head
	cd backend/notification-service && alembic upgrade head

db-reset: ## Reset database
	docker-compose down -v
	docker-compose up -d postgres redis
	sleep 10
	$(MAKE) db-migrate

# Docker
build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs for all services
	docker-compose logs -f

logs-service: ## Show logs for specific service (usage: make logs-service SERVICE=inventory-service)
	docker-compose logs -f $(SERVICE)

# Shell access
shell: ## Access shell in running container
	docker-compose exec $(SERVICE) /bin/bash

shell-db: ## Access PostgreSQL shell
	docker-compose exec postgres psql -U postgres -d microservices_db

shell-redis: ## Access Redis shell
	docker-compose exec redis redis-cli

# Monitoring
monitor: ## Start monitoring stack
	docker-compose up -d prometheus grafana

# Cleanup
clean: ## Clean up containers and volumes
	docker-compose down -v
	docker system prune -f

clean-all: ## Clean up everything including images
	docker-compose down -v --rmi all
	docker system prune -af

# Pre-commit
pre-commit-install: ## Install pre-commit hooks
	pre-commit install

pre-commit-run: ## Run pre-commit on all files
	pre-commit run --all-files

# Kubernetes
k8s-apply: ## Apply Kubernetes manifests
	kubectl apply -f k8s/

k8s-delete: ## Delete Kubernetes resources
	kubectl delete -f k8s/

# Helm
helm-install: ## Install Helm charts
	helm install microservices-app helm/microservices-app

helm-upgrade: ## Upgrade Helm charts
	helm upgrade microservices-app helm/microservices-app

helm-uninstall: ## Uninstall Helm charts
	helm uninstall microservices-app

# Security
security-scan: ## Run security scans
	safety check
	cd frontend && npm audit

# Documentation
docs: ## Generate documentation
	cd docs && make html

# Performance
perf-test: ## Run performance tests
	cd scripts/performance && python load_test.py

# Backup
backup: ## Backup database
	./scripts/maintenance/backup-database.sh

# Health check
health: ## Check service health
	./scripts/maintenance/health-check.sh
