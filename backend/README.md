# CDST Diagnostic Network Optimization Platform - Backend

## Overview

The backend for the CDST Diagnostic Network Optimization Platform is a high-performance FastAPI application designed to optimize laboratory network allocations for Culture and Drug Sensitivity Testing (CDST) in healthcare systems.

**Developed by PATH** - Program for Appropriate Technology in Health

## 🚀 Features

### Core Functionality
- **Multi-Objective Optimization**: NSGA-II algorithm for laboratory allocation optimization
- **Geospatial Analysis**: PostGIS integration for geographic calculations
- **Real-time Routing**: OSRM integration with Haversine fallback
- **Role-Based Access Control**: Comprehensive authentication and authorization
- **Data Import/Export**: Support for CSV, Excel, and JSON formats
- **Background Processing**: Celery-based task queue for long-running operations

### Technical Highlights
- **FastAPI Framework**: High-performance async API with automatic OpenAPI documentation
- **PostgreSQL + PostGIS**: Robust database with geospatial capabilities
- **Redis Caching**: High-performance caching and session management
- **OR-Tools Optimization**: Google's optimization library for complex problem solving
- **Docker Support**: Full containerization with multi-stage builds
- **Monitoring**: Prometheus metrics and structured logging

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Load Balancer │    │   Monitoring    │
│   (Streamlit)   │    │     (Nginx)     │    │ (Prometheus)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────┐
         │              FastAPI Backend                    │
         └─────────────────────────────────────────────────┘
                                 │
    ┌────────────────────────────┼────────────────────────────┐
    │                            │                            │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │      Redis      │    │   Celery        │
│   + PostGIS     │    │    (Cache)      │    │   Workers       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Requirements

### System Requirements
- Python 3.11+
- PostgreSQL 15+ with PostGIS extension
- Redis 7.0+
- Docker and Docker Compose (recommended)

### Hardware Recommendations
- **Development**: 4GB RAM, 2 CPU cores, 10GB storage
- **Production**: 16GB RAM, 8 CPU cores, 100GB SSD storage

## 🛠️ Installation

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cdst-optimization-platform
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the services**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Create initial admin user**
   ```bash
   docker-compose exec backend python -m app.scripts.create_admin
   ```

### Option 2: Local Development

1. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL with PostGIS**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql-15 postgresql-15-postgis-3
   
   # Create database
   sudo -u postgres createdb cdst_optimization
   sudo -u postgres psql -d cdst_optimization -c "CREATE EXTENSION postgis;"
   ```

3. **Set up Redis**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server
   sudo systemctl start redis-server
   ```

4. **Configure environment**
   ```bash
   export DATABASE_URL="postgresql://cdst_user:cdst_password@localhost/cdst_optimization"
   export REDIS_URL="redis://localhost:6379/0"
   export SECRET_KEY="your-secret-key"
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` | Yes |
| `SECRET_KEY` | JWT signing key | - | Yes |
| `DEBUG` | Enable debug mode | `false` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `OSRM_BASE_URL` | OSRM routing service URL | `http://router.project-osrm.org` | No |
| `ENABLE_OPTIMIZATION` | Enable optimization features | `true` | No |
| `OPTIMIZATION_POPULATION_SIZE` | NSGA-II population size | `200` | No |
| `OPTIMIZATION_MAX_GENERATIONS` | NSGA-II max generations | `500` | No |

### Database Configuration

The application uses PostgreSQL with PostGIS for geospatial data. Key configurations:

- **Connection Pool**: 10 connections with 20 overflow
- **Extensions**: PostGIS, PostGIS Topology
- **Encoding**: UTF-8
- **Timezone**: UTC

### Optimization Engine Configuration

The NSGA-II optimization engine can be configured through environment variables:

```bash
# Population and generation settings
OPTIMIZATION_POPULATION_SIZE=200
OPTIMIZATION_MAX_GENERATIONS=500
OPTIMIZATION_TIMEOUT=900  # 15 minutes

# Objective weights (must sum to 1.0)
DEFAULT_DISTANCE_WEIGHT=0.3
DEFAULT_TIME_WEIGHT=0.2
DEFAULT_COST_WEIGHT=0.25
DEFAULT_UTILIZATION_WEIGHT=0.15
DEFAULT_ACCESSIBILITY_WEIGHT=0.1
```

## 📚 API Documentation

### Authentication

The API uses JWT-based authentication with role-based access control.

#### Login
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 691200
}
```

### Core Endpoints

#### Networks
- `GET /api/v1/networks` - List laboratory networks
- `POST /api/v1/networks` - Create new network
- `GET /api/v1/networks/{id}` - Get network details
- `PUT /api/v1/networks/{id}` - Update network
- `DELETE /api/v1/networks/{id}` - Delete network

#### Laboratories
- `GET /api/v1/networks/{network_id}/laboratories` - List laboratories
- `POST /api/v1/networks/{network_id}/laboratories` - Add laboratory
- `GET /api/v1/laboratories/{id}` - Get laboratory details
- `PUT /api/v1/laboratories/{id}` - Update laboratory
- `DELETE /api/v1/laboratories/{id}` - Delete laboratory

#### Optimization
- `POST /api/v1/networks/{network_id}/scenarios` - Create optimization scenario
- `GET /api/v1/scenarios/{id}` - Get scenario details
- `POST /api/v1/scenarios/{id}/run` - Execute optimization
- `GET /api/v1/scenarios/{id}/results` - Get optimization results
- `GET /api/v1/scenarios/{id}/progress` - Get optimization progress

#### Data Import/Export
- `POST /api/v1/upload` - Upload data files
- `GET /api/v1/export/network/{id}` - Export network data
- `GET /api/v1/templates/{type}` - Download data templates

### WebSocket Endpoints

Real-time updates for optimization progress:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/optimization/{scenario_id}');
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Progress:', data.progress);
};
```

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_optimization.py

# Run with verbose output
pytest -v
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **Performance Tests**: Optimization algorithm benchmarks
- **End-to-End Tests**: Complete workflow testing

### Test Data

Sample test data is provided in the `tests/data/` directory:

- `sample_laboratories.json` - Laboratory test data
- `sample_service_areas.json` - Service area test data
- `sample_test_demands.json` - Test demand data

## 📊 Monitoring and Logging

### Structured Logging

The application uses structured logging with the following levels:

- **DEBUG**: Detailed diagnostic information
- **INFO**: General application flow
- **WARNING**: Potential issues or degraded performance
- **ERROR**: Error conditions that don't stop the application
- **CRITICAL**: Serious errors that may abort the application

### Metrics

Prometheus metrics are exposed at `/metrics`:

- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request duration histogram
- `optimization_runs_total` - Total optimization runs
- `optimization_duration_seconds` - Optimization duration histogram
- `database_connections_active` - Active database connections

### Health Checks

- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed health check with dependencies

## 🚀 Deployment

### Production Deployment with Docker

1. **Build production image**
   ```bash
   docker build -t cdst-backend:latest .
   ```

2. **Run with production settings**
   ```bash
   docker run -d \
     --name cdst-backend \
     -p 8000:8000 \
     -e DATABASE_URL="postgresql://user:pass@host/db" \
     -e REDIS_URL="redis://host:6379/0" \
     -e SECRET_KEY="production-secret-key" \
     -e DEBUG="false" \
     cdst-backend:latest
   ```

### Kubernetes Deployment

Kubernetes manifests are provided in the `deployment/k8s/` directory:

```bash
kubectl apply -f deployment/k8s/
```

### Performance Tuning

For production deployments, consider these optimizations:

1. **Database Connection Pooling**
   ```bash
   DATABASE_POOL_SIZE=20
   DATABASE_MAX_OVERFLOW=40
   ```

2. **Worker Processes**
   ```bash
   # For CPU-bound workloads
   uvicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```

3. **Optimization Settings**
   ```bash
   # Reduce for faster results, increase for better quality
   OPTIMIZATION_POPULATION_SIZE=100
   OPTIMIZATION_MAX_GENERATIONS=250
   ```

## 🔒 Security

### Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt with salt
- **Rate Limiting**: Configurable rate limits for API endpoints
- **CORS Protection**: Configurable cross-origin resource sharing
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **Input Validation**: Pydantic model validation
- **Security Headers**: Comprehensive HTTP security headers

### Security Configuration

```bash
# Authentication settings
ACCESS_TOKEN_EXPIRE_MINUTES=480  # 8 hours
REFRESH_TOKEN_EXPIRE_MINUTES=43200  # 30 days
PASSWORD_MIN_LENGTH=8
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=900  # 15 minutes

# Rate limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_BURST=100
```

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Run tests**
   ```bash
   pytest
   ```

6. **Submit a pull request**

### Code Style

The project uses:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run code quality checks:
```bash
black app/
isort app/
flake8 app/
mypy app/
```

## 📄 License

Copyright © 2024 PATH. All rights reserved.

This software is proprietary and confidential. Unauthorized copying, distribution, or modification is strictly prohibited.

## 🆘 Support

### Documentation
- [API Documentation](http://localhost:8000/docs) (when running locally)
- [Technical Specifications](../docs/technical-requirements.md)
- [User Stories](../docs/user-stories.md)

### Getting Help

1. **Check the logs**
   ```bash
   docker-compose logs backend
   ```

2. **Health check**
   ```bash
   curl http://localhost:8000/health/detailed
   ```

3. **Database connection**
   ```bash
   docker-compose exec database psql -U cdst_user -d cdst_optimization
   ```

### Common Issues

#### Database Connection Issues
```bash
# Check if PostGIS extension is installed
docker-compose exec database psql -U cdst_user -d cdst_optimization -c "SELECT PostGIS_Version();"
```

#### Optimization Performance
```bash
# Monitor optimization progress
curl http://localhost:8000/api/v1/scenarios/{id}/progress
```

#### Redis Connection Issues
```bash
# Test Redis connection
docker-compose exec redis redis-cli ping
```

---

**Built with ❤️ by PATH for global health equity**