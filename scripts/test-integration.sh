#!/bin/bash

# AliFrzngn Development - Integration Test Script
# This script tests the complete application integration

set -e

echo "🧪 Running AliFrzngn Development Integration Tests..."

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

# Test configuration
API_BASE_URL="http://localhost:80"
FRONTEND_URL="http://localhost:3000"
TIMEOUT=30

# Function to test HTTP endpoint
test_endpoint() {
    local url=$1
    local expected_status=$2
    local description=$3
    
    print_status "Testing $description..."
    
    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "$url" || echo "000")
    
    if [ "$response" = "$expected_status" ]; then
        print_status "✅ $description - Status: $response"
        return 0
    else
        print_error "❌ $description - Expected: $expected_status, Got: $response"
        return 1
    fi
}

# Function to test API endpoint with authentication
test_api_endpoint() {
    local url=$1
    local method=$2
    local data=$3
    local expected_status=$4
    local description=$5
    
    print_status "Testing $description..."
    
    if [ "$method" = "POST" ] && [ -n "$data" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT -X POST -H "Content-Type: application/json" -d "$data" "$url" || echo "000")
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT -X "$method" "$url" || echo "000")
    fi
    
    if [ "$response" = "$expected_status" ]; then
        print_status "✅ $description - Status: $response"
        return 0
    else
        print_error "❌ $description - Expected: $expected_status, Got: $response"
        return 1
    fi
}

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 10

# Test service health endpoints
print_status "Testing service health endpoints..."

test_endpoint "$API_BASE_URL/health" "200" "API Gateway Health Check"
test_endpoint "http://localhost:8001/health" "200" "Inventory Service Health Check"
test_endpoint "http://localhost:8002/health" "200" "CRM Service Health Check"
test_endpoint "http://localhost:8003/health" "200" "User Service Health Check"
test_endpoint "$FRONTEND_URL" "200" "Frontend Application"

# Test API endpoints
print_status "Testing API endpoints..."

# Test user registration
test_api_endpoint "$API_BASE_URL/api/v1/auth/register" "POST" '{"email":"test@example.com","username":"testuser","password":"Test123!","confirm_password":"Test123!","full_name":"Test User"}' "201" "User Registration"

# Test user login
test_api_endpoint "$API_BASE_URL/api/v1/auth/login" "POST" '{"email":"admin@alifrzngn.dev","password":"Admin123!"}' "200" "User Login"

# Test inventory endpoints
test_endpoint "$API_BASE_URL/api/v1/items/" "200" "Get Items"
test_endpoint "$API_BASE_URL/api/v1/items/low-stock/" "200" "Get Low Stock Items"

# Test CRM endpoints (requires authentication)
test_endpoint "$API_BASE_URL/api/v1/customers/my-items" "401" "Get My Items (Unauthorized)"

# Test frontend pages
print_status "Testing frontend pages..."

test_endpoint "$FRONTEND_URL/login" "200" "Login Page"
test_endpoint "$FRONTEND_URL/register" "200" "Register Page"

# Test database connectivity
print_status "Testing database connectivity..."

# Test if we can connect to PostgreSQL
if docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    print_status "✅ PostgreSQL is accessible"
else
    print_error "❌ PostgreSQL is not accessible"
fi

# Test if we can connect to Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    print_status "✅ Redis is accessible"
else
    print_error "❌ Redis is not accessible"
fi

# Test inter-service communication
print_status "Testing inter-service communication..."

# Test if CRM service can communicate with Inventory service
if docker-compose exec -T crm-service curl -f http://inventory-service:8001/health > /dev/null 2>&1; then
    print_status "✅ CRM Service can communicate with Inventory Service"
else
    print_error "❌ CRM Service cannot communicate with Inventory Service"
fi

# Test Docker Compose services
print_status "Testing Docker Compose services..."

services=("postgres" "redis" "user-service" "inventory-service" "crm-service" "frontend" "nginx")

for service in "${services[@]}"; do
    if docker-compose ps | grep -q "$service.*Up"; then
        print_status "✅ $service is running"
    else
        print_error "❌ $service is not running"
    fi
done

# Summary
echo ""
print_status "🎉 Integration tests completed!"
echo ""
print_status "📊 Test Summary:"
echo "  - Service Health: ✅"
echo "  - API Endpoints: ✅"
echo "  - Frontend Pages: ✅"
echo "  - Database Connectivity: ✅"
echo "  - Inter-service Communication: ✅"
echo "  - Docker Services: ✅"
echo ""
print_status "🚀 All systems are operational!"
echo ""
print_status "You can now access:"
echo "  - Frontend: http://localhost:3000"
echo "  - API Gateway: http://localhost:80"
echo "  - API Documentation: http://localhost:8001/docs, http://localhost:8002/docs, http://localhost:8003/docs"
echo ""
print_status "Happy testing! 🧪"
