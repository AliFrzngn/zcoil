#!/bin/bash

# AliFrzngn Development - Setup Script
# This script sets up the complete development environment

set -e

echo "🚀 Setting up AliFrzngn Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p data/postgres
mkdir -p data/redis

# Set up environment file
if [ ! -f .env ]; then
    print_status "Creating .env file..."
    cp .env.example .env
    print_warning "Please review and update the .env file with your configuration."
fi

# Build and start services
print_status "Building Docker images..."
docker-compose build

print_status "Starting services..."
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 30

# Check service health
print_status "Checking service health..."

services=("postgres:5432" "redis:6379" "user-service:8003" "inventory-service:8001" "crm-service:8002" "nginx:80")

for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if docker-compose exec -T $name curl -f http://localhost:$port/health > /dev/null 2>&1; then
        print_status "✅ $name is healthy"
    else
        print_warning "⚠️  $name health check failed"
    fi
done

# Run database migrations
print_status "Running database migrations..."
docker-compose exec migrate python backend/shared/database/migrate.py upgrade

# Display service URLs
echo ""
print_status "🎉 Setup complete! Services are running:"
echo ""
echo "📊 Frontend Application: http://localhost:3000"
echo "🔗 API Gateway: http://localhost:80"
echo "👤 User Service: http://localhost:8003"
echo "📦 Inventory Service: http://localhost:8001"
echo "🤝 CRM Service: http://localhost:8002"
echo "🗄️  PostgreSQL: localhost:5432"
echo "⚡ Redis: localhost:6379"
echo ""
echo "📚 API Documentation:"
echo "  - User Service: http://localhost:8003/docs"
echo "  - Inventory Service: http://localhost:8001/docs"
echo "  - CRM Service: http://localhost:8002/docs"
echo ""
echo "🔑 Default Admin Credentials:"
echo "  Email: admin@alifrzngn.dev"
echo "  Password: Admin123!"
echo ""
echo "📝 To stop all services: docker-compose down"
echo "📝 To view logs: docker-compose logs -f [service-name]"
echo "📝 To restart a service: docker-compose restart [service-name]"
echo ""
print_status "Happy coding! 🚀"
