# AliFrzngn Development - Makefile
# Common commands for development and deployment

.PHONY: help setup build up down logs test clean restart status

<<<<<<< Current (Your changes)
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
=======
# Default target
help:
	@echo "AliFrzngn Development - Available Commands:"
	@echo ""
	@echo "🚀 Setup & Development:"
	@echo "  setup          - Set up the complete development environment"
	@echo "  build          - Build all Docker images"
	@echo "  up             - Start all services"
	@echo "  down           - Stop all services"
	@echo "  restart        - Restart all services"
	@echo "  status         - Show service status"
	@echo ""
	@echo "🔍 Monitoring & Debugging:"
	@echo "  logs           - Show logs for all services"
	@echo "  logs-service   - Show logs for specific service (make logs-service SERVICE=user-service)"
	@echo "  shell          - Open shell in specific service (make shell SERVICE=user-service)"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  test           - Run integration tests"
	@echo "  test-unit      - Run unit tests"
	@echo "  test-frontend  - Run frontend tests"
	@echo ""
	@echo "🗄️  Database:"
	@echo "  migrate        - Run database migrations"
	@echo "  migrate-create - Create new migration (make migrate-create MESSAGE='description')"
	@echo "  db-reset       - Reset database"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  clean          - Clean up containers and volumes"
	@echo "  clean-images   - Remove unused Docker images"
	@echo "  clean-volumes  - Remove unused Docker volumes"

# Setup development environment
setup:
	@echo "🚀 Setting up AliFrzngn Development Environment..."
	@./scripts/setup.sh

# Build all Docker images
build:
	@echo "🔨 Building Docker images..."
	@docker-compose build

# Start all services
up:
	@echo "🚀 Starting all services..."
	@docker-compose up -d

# Stop all services
down:
	@echo "🛑 Stopping all services..."
	@docker-compose down

# Restart all services
restart:
	@echo "🔄 Restarting all services..."
	@docker-compose restart

# Show service status
status:
	@echo "📊 Service Status:"
	@docker-compose ps

# Show logs for all services
logs:
	@echo "📋 Showing logs for all services..."
	@docker-compose logs -f

# Show logs for specific service
logs-service:
	@echo "📋 Showing logs for $(SERVICE)..."
	@docker-compose logs -f $(SERVICE)

# Open shell in specific service
shell:
	@echo "🐚 Opening shell in $(SERVICE)..."
	@docker-compose exec $(SERVICE) /bin/bash

# Run integration tests
test:
	@echo "🧪 Running integration tests..."
	@./scripts/test-integration.sh

# Run unit tests
test-unit:
	@echo "🧪 Running unit tests..."
	@docker-compose exec user-service python -m pytest backend/user-service/tests/ -v
	@docker-compose exec inventory-service python -m pytest backend/inventory-service/tests/ -v
	@docker-compose exec crm-service python -m pytest backend/crm-service/tests/ -v

# Run frontend tests
test-frontend:
	@echo "🧪 Running frontend tests..."
	@docker-compose exec frontend npm test

# Run database migrations
migrate:
	@echo "🗄️  Running database migrations..."
	@docker-compose exec migrate python backend/shared/database/migrate.py upgrade

# Create new migration
migrate-create:
	@echo "🗄️  Creating new migration: $(MESSAGE)"
	@docker-compose exec migrate python backend/shared/database/migrate.py create "$(MESSAGE)"

# Reset database
db-reset:
	@echo "🗄️  Resetting database..."
	@docker-compose down -v
	@docker-compose up -d postgres redis
	@sleep 10
	@docker-compose run --rm migrate python backend/shared/database/migrate.py upgrade

# Clean up containers and volumes
clean:
	@echo "🧹 Cleaning up containers and volumes..."
	@docker-compose down -v
	@docker system prune -f

# Clean up unused Docker images
clean-images:
	@echo "🧹 Cleaning up unused Docker images..."
	@docker image prune -f

# Clean up unused Docker volumes
clean-volumes:
	@echo "🧹 Cleaning up unused Docker volumes..."
	@docker volume prune -f

# Development shortcuts
dev: up logs
dev-full: setup up logs
dev-restart: restart logs

# Quick service management
start-service:
	@echo "🚀 Starting $(SERVICE)..."
	@docker-compose up -d $(SERVICE)

stop-service:
	@echo "🛑 Stopping $(SERVICE)..."
	@docker-compose stop $(SERVICE)

restart-service:
	@echo "🔄 Restarting $(SERVICE)..."
	@docker-compose restart $(SERVICE)
>>>>>>> Incoming (Background Agent changes)
