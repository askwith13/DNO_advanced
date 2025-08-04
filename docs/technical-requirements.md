# Technical Requirements - CDST Diagnostic Network Optimization Platform

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │     FastAPI     │    │   PostgreSQL    │
│   Frontend      │◄──►│    Backend      │◄──►│   Database      │
│                 │    │                 │    │   + PostGIS     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Leaflet Maps  │    │   OR-Tools      │    │   OpenStreetMap │
│   Visualization │    │   Optimization  │    │   Routing API   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1.2 Component Specifications

#### Frontend (Streamlit)
- **Framework**: Streamlit 1.28+
- **Responsive Design**: Desktop-optimized (1920x1080 primary target)
- **Pages**:
  - Dashboard (overview and quick actions)
  - Data Input (file upload and validation)
  - Optimization Configuration (parameter settings)
  - Results Visualization (maps and analytics)
  - Reports (downloadable outputs)
  - About (PATH organization information)

#### Backend (FastAPI)
- **Framework**: FastAPI 0.104+
- **Python Version**: 3.11+
- **Key Features**:
  - RESTful API endpoints
  - Async/await support for concurrent operations
  - Automatic API documentation (OpenAPI/Swagger)
  - Input validation with Pydantic models
  - Background task processing

#### Database (PostgreSQL + PostGIS)
- **Version**: PostgreSQL 15+ with PostGIS 3.3+
- **Features**:
  - Geospatial data support
  - ACID compliance
  - Advanced indexing (B-tree, GiST, GIN)
  - JSON/JSONB support for flexible schemas

## 2. Performance Requirements

### 2.1 Scalability Targets
- **Laboratory Networks**: Support 100+ laboratories per optimization
- **Test Allocations**: Process 10,000+ simultaneous allocations
- **Geographic Regions**: Multi-region support with timezone handling
- **Concurrent Users**: 50+ simultaneous users

### 2.2 Performance Standards
- **Optimization Completion**: ≤ 15 minutes for networks with 100 laboratories
- **API Response Time**: ≤ 2 seconds for standard queries
- **File Upload Processing**: ≤ 30 seconds for 10MB files
- **Map Rendering**: ≤ 3 seconds for complex visualizations
- **System Availability**: 99.9% uptime (8.76 hours downtime/year)

### 2.3 Resource Requirements
- **CPU**: Multi-core processing for optimization algorithms
- **Memory**: 8GB+ RAM for large network optimizations
- **Storage**: 100GB+ for data, logs, and temporary files
- **Network**: High-speed internet for routing API calls

## 3. Data Requirements

### 3.1 Input Data Specifications

#### Laboratory Network Data
```json
{
  "laboratory_id": "string (unique)",
  "name": "string (required)",
  "coordinates": {
    "latitude": "float (-90 to 90)",
    "longitude": "float (-180 to 180)"
  },
  "contact_info": {
    "address": "string",
    "phone": "string",
    "email": "string"
  },
  "operational_hours": {
    "monday": {"open": "HH:MM", "close": "HH:MM"},
    "tuesday": {"open": "HH:MM", "close": "HH:MM"}
    // ... other days
  },
  "capacities": {
    "max_tests_per_day": "integer (>0)",
    "max_tests_per_month": "integer (>0)",
    "staff_count": "integer (>0)"
  },
  "test_capabilities": [
    {
      "test_type": "string",
      "available": "boolean",
      "time_per_test_minutes": "integer",
      "staff_required": "integer",
      "equipment_utilization": "float (0-1)"
    }
  ]
}
```

#### Geographic and Routing Data
- **Coordinate System**: WGS84 (EPSG:4326)
- **Precision**: 6 decimal places (~0.1 meter accuracy)
- **Routing API**: OpenStreetMap Routing Machine (OSRM)
- **Fallback**: Haversine distance calculation
- **Caching**: Redis for route caching (TTL: 24 hours)

### 3.2 Data Validation Rules
- **Coordinates**: Valid latitude/longitude ranges
- **Capacities**: Positive integers only
- **Test Times**: Realistic time ranges (5-480 minutes)
- **Staff Requirements**: Cannot exceed total staff count
- **File Formats**: CSV, Excel (.xlsx), JSON with size limits (50MB)

## 4. Security Requirements

### 4.1 Authentication & Authorization
- **User Authentication**: JWT-based authentication
- **Role-Based Access Control (RBAC)**:
  - Administrator: Full system access
  - Analyst: Data input and optimization
  - Viewer: Read-only access to results
- **Session Management**: 8-hour session timeout
- **Password Policy**: Minimum 12 characters, complexity requirements

### 4.2 Data Protection
- **Encryption at Rest**: AES-256 for database
- **Encryption in Transit**: TLS 1.3 for all communications
- **Data Anonymization**: Optional PII masking features
- **Audit Logging**: All user actions and optimization decisions
- **Backup & Recovery**: Daily automated backups with 30-day retention

### 4.3 Compliance
- **Healthcare Data Standards**: HIPAA compliance considerations
- **Data Residency**: Configurable data storage location
- **Privacy Controls**: User consent management
- **Audit Trail**: Immutable log of all system changes

## 5. Integration Requirements

### 5.1 External APIs
- **OpenStreetMap Routing API**:
  - Primary routing service
  - Rate limiting: 1000 requests/hour
  - Error handling with automatic fallback
- **Haversine Distance Calculation**:
  - Fallback when routing API unavailable
  - Configurable accuracy parameters
- **Future Integrations**:
  - Laboratory Information Systems (LIS)
  - Hospital Management Systems (HMS)
  - Supply Chain Management systems

### 5.2 Data Export/Import
- **Export Formats**: CSV, Excel, JSON, PDF reports
- **Import Validation**: Real-time error checking
- **Batch Processing**: Queue-based processing for large files
- **API Endpoints**: RESTful API for programmatic access

## 6. Optimization Engine Specifications

### 6.1 Algorithm Requirements
- **Primary Algorithm**: NSGA-II (Non-dominated Sorting Genetic Algorithm II)
- **Alternative Algorithms**: MOEA/D, SPEA2 for comparison
- **Objective Functions**:
  1. Distance minimization (weighted: 25%)
  2. Time optimization (weighted: 20%)
  3. Cost reduction (weighted: 25%)
  4. Utilization maximization (weighted: 20%)
  5. Accessibility enhancement (weighted: 10%)

### 6.2 Constraints Handling
- **Hard Constraints**: Cannot be violated
  - Laboratory capacity limits
  - Staff availability windows
  - Equipment maintenance schedules
- **Soft Constraints**: Preferential but can be violated
  - Quality assurance preferences
  - Cost optimization targets
  - Geographic preferences

### 6.3 Optimization Parameters
- **Population Size**: 100-500 individuals
- **Generations**: 100-1000 iterations
- **Crossover Rate**: 0.8-0.95
- **Mutation Rate**: 0.01-0.1
- **Selection Method**: Tournament selection
- **Termination Criteria**: 
  - Maximum generations reached
  - Convergence threshold met
  - Time limit exceeded (15 minutes)

## 7. Monitoring and Logging

### 7.1 Application Monitoring
- **Performance Metrics**: Response times, throughput, error rates
- **System Health**: CPU, memory, disk usage
- **User Analytics**: Feature usage, session duration
- **Optimization Metrics**: Algorithm performance, convergence rates

### 7.2 Logging Requirements
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Rotation**: Daily rotation with compression
- **Log Retention**: 90 days for application logs, 1 year for audit logs
- **Structured Logging**: JSON format for machine parsing

### 7.3 Alerting
- **System Alerts**: High resource usage, service failures
- **Business Alerts**: Optimization failures, data quality issues
- **Notification Channels**: Email, Slack, webhook integrations
- **Escalation Policies**: Tiered response based on severity

## 8. Deployment and Infrastructure

### 8.1 Container Strategy
- **Containerization**: Docker containers for all services
- **Orchestration**: Docker Compose for development, Kubernetes for production
- **Base Images**: Official Python, PostgreSQL, Redis images
- **Multi-stage Builds**: Optimized container sizes

### 8.2 Environment Configuration
- **Development**: Local Docker Compose setup
- **Staging**: Cloud-based testing environment
- **Production**: High-availability cluster deployment
- **Configuration Management**: Environment variables, secrets management

### 8.3 Scalability Strategy
- **Horizontal Scaling**: Load balancer with multiple backend instances
- **Database Scaling**: Read replicas for query optimization
- **Caching Strategy**: Redis for session and route caching
- **CDN Integration**: Static asset delivery optimization