# Microservices Application

A production-ready microservices-based web application built with modern technologies and best practices.

## 🏗️ Architecture

This application follows a microservices architecture with the following components:

### Backend Services
- **Inventory Service** - Product and inventory management
- **CRM Service** - Customer relationship management
- **User Service** - Authentication and user management
- **Notification Service** - Email, SMS, and push notifications

### Frontend
- **Next.js 13+** with App Router
- **TypeScript** for type safety
- **TailwindCSS** for styling
- **TanStack Query** for data fetching
- **Redux Toolkit** for state management

### Infrastructure
- **Docker** & **Docker Compose** for containerization
- **Kubernetes** for orchestration
- **Helm** for package management
- **Nginx** as API Gateway
- **PostgreSQL** for data persistence
- **Redis** for caching and sessions

### Monitoring & Observability
- **Prometheus** for metrics collection
- **Grafana** for visualization
- **ELK Stack** for logging
- **Sentry** for error tracking
- **Jaeger** for distributed tracing

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd microservices-app
   ```

2. **Install dependencies**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install Frontend dependencies
   cd frontend
   npm install
   cd ..
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start the development environment**
   ```bash
   # Start all services with Docker Compose
   docker-compose up -d
   
   # Or start individual services for development
   make dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:80
   - Inventory Service: http://localhost:8001
   - CRM Service: http://localhost:8002
   - User Service: http://localhost:8003
   - Notification Service: http://localhost:8004

## 📁 Project Structure

```
microservices-app/
├── backend/                 # Backend microservices
│   ├── shared/             # Shared utilities and common code
│   ├── inventory-service/  # Inventory management service
│   ├── crm-service/        # CRM service
│   ├── user-service/       # User management service
│   └── notification-service/ # Notification service
├── frontend/               # Next.js frontend application
├── nginx/                  # Nginx configuration
├── k8s/                    # Kubernetes manifests
├── helm/                   # Helm charts
├── ci-cd/                  # CI/CD pipelines
├── monitoring/             # Monitoring configurations
├── infrastructure/         # Infrastructure as Code
├── docker/                 # Docker configurations
├── scripts/                # Utility scripts
└── docs/                   # Documentation
```

## 🛠️ Development

### Available Commands

```bash
# Development
make dev              # Start development environment
make dev-full         # Start full environment with all services

# Testing
make test             # Run all tests
make test-unit        # Run unit tests only
make test-integration # Run integration tests
make test-frontend    # Run frontend tests

# Code Quality
make lint             # Run linting
make format           # Format code
make type-check       # Run type checking

# Database
make db-migrate       # Run database migrations
make db-reset         # Reset database

# Docker
make build            # Build all Docker images
make up               # Start all services
make down             # Stop all services
make logs             # Show logs

# Monitoring
make monitor          # Start monitoring stack
```

### Code Standards

- **Python**: Black, isort, flake8, mypy
- **TypeScript**: ESLint, Prettier
- **Pre-commit hooks** for automated code quality checks

## 🚀 Deployment

### Local Deployment
```bash
docker-compose up -d
```

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Or use Helm
helm install microservices-app helm/microservices-app
```

### Production Deployment
See [deployment documentation](docs/deployment/production-deployment.md) for detailed production deployment instructions.

## 📊 Monitoring

### Access Monitoring Tools
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)
- **Kibana**: http://localhost:5601

### Health Checks
- **Application**: http://localhost/health
- **Individual Services**: 
  - Inventory: http://localhost:8001/health
  - CRM: http://localhost:8002/health
  - User: http://localhost:8003/health
  - Notification: http://localhost:8004/health

## 🔧 Configuration

### Environment Variables
See `.env.example` for all available configuration options.

### Key Configuration Areas
- Database connections
- Redis configuration
- JWT settings
- CORS origins
- Monitoring endpoints
- External service credentials

## 🧪 Testing

### Running Tests
```bash
# All tests
make test

# Backend only
pytest backend/ --cov=backend

# Frontend only
cd frontend && npm test
```

### Test Coverage
- Backend: Aim for >90% coverage
- Frontend: Aim for >80% coverage

## 📚 Documentation

- [Architecture Overview](docs/architecture/microservices-architecture.md)
- [API Documentation](docs/api/)
- [Deployment Guide](docs/deployment/)
- [Development Guide](docs/development/)
- [Operations Guide](docs/operations/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

See [contributing guidelines](docs/development/contributing.md) for more details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the troubleshooting guide

## 🔄 Version History

- **v1.0.0** - Initial release with core microservices
- **v1.1.0** - Added monitoring and observability
- **v1.2.0** - Enhanced security and performance

---

Built with ❤️ using modern microservices architecture and best practices.