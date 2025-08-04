# API Specifications - CDST Diagnostic Network Optimization Platform

## Base URL
```
Production: https://api.cdst-optimization.path.org/v1
Development: http://localhost:8000/v1
```

## Authentication
All API endpoints (except health check and authentication) require JWT authentication.

**Header**: `Authorization: Bearer <jwt_token>`

## Response Format
All API responses follow a consistent format:

```json
{
  "success": true,
  "data": {},
  "message": "Success message",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

Error responses:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {}
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `422` - Validation Error
- `429` - Rate Limited
- `500` - Internal Server Error

---

## 1. Authentication Endpoints

### POST /auth/login
Authenticate user and return JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "expires_in": 28800,
    "user": {
      "id": "uuid",
      "username": "string",
      "email": "string",
      "role": "administrator|analyst|viewer",
      "first_name": "string",
      "last_name": "string",
      "organization": "string"
    }
  }
}
```

### POST /auth/logout
Invalidate current JWT token.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

### POST /auth/refresh
Refresh JWT token.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "string",
    "expires_in": 28800
  }
}
```

---

## 2. User Management Endpoints

### GET /users
List all users (Admin only).

**Query Parameters:**
- `page` (integer, default: 1)
- `limit` (integer, default: 20, max: 100)
- `role` (string, optional): Filter by role
- `search` (string, optional): Search by username, email, or name

**Response:**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": "uuid",
        "username": "string",
        "email": "string",
        "role": "string",
        "first_name": "string",
        "last_name": "string",
        "organization": "string",
        "is_active": true,
        "created_at": "2024-01-01T12:00:00Z",
        "last_login": "2024-01-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "pages": 5
    }
  }
}
```

### POST /users
Create new user (Admin only).

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "administrator|analyst|viewer",
  "first_name": "string",
  "last_name": "string",
  "organization": "string"
}
```

### GET /users/{user_id}
Get user details.

### PUT /users/{user_id}
Update user (Admin or self).

### DELETE /users/{user_id}
Deactivate user (Admin only).

---

## 3. Laboratory Network Endpoints

### GET /networks
List laboratory networks.

**Query Parameters:**
- `page` (integer, default: 1)
- `limit` (integer, default: 20)
- `search` (string, optional)
- `is_active` (boolean, optional)

**Response:**
```json
{
  "success": true,
  "data": {
    "networks": [
      {
        "id": "uuid",
        "name": "string",
        "description": "string",
        "created_by": "uuid",
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z",
        "is_active": true,
        "laboratory_count": 15,
        "service_area_count": 25
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 5,
      "pages": 1
    }
  }
}
```

### POST /networks
Create new laboratory network.

**Request Body:**
```json
{
  "name": "string",
  "description": "string"
}
```

### GET /networks/{network_id}
Get network details with statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "string",
    "description": "string",
    "created_by": "uuid",
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z",
    "is_active": true,
    "statistics": {
      "total_laboratories": 15,
      "total_service_areas": 25,
      "total_test_types": 7,
      "average_distance_km": 12.5,
      "average_utilization": 0.75,
      "total_monthly_capacity": 5000,
      "coverage_percentage": 85.2
    }
  }
}
```

### PUT /networks/{network_id}
Update network.

### DELETE /networks/{network_id}
Deactivate network.

---

## 4. Laboratory Endpoints

### GET /networks/{network_id}/laboratories
List laboratories in network.

**Query Parameters:**
- `page` (integer, default: 1)
- `limit` (integer, default: 50)
- `search` (string, optional)
- `test_type_id` (uuid, optional): Filter by test capability
- `min_capacity` (integer, optional)
- `bbox` (string, optional): Bounding box filter "lat1,lng1,lat2,lng2"

**Response:**
```json
{
  "success": true,
  "data": {
    "laboratories": [
      {
        "id": "uuid",
        "laboratory_id": "LAB001",
        "name": "Central Laboratory",
        "coordinates": {
          "latitude": 40.7128,
          "longitude": -74.0060
        },
        "address": "123 Main St, City, State",
        "phone": "+1-555-0123",
        "email": "lab@example.com",
        "created_at": "2024-01-01T12:00:00Z",
        "capacities": {
          "max_tests_per_day": 100,
          "max_tests_per_month": 2500,
          "staff_count": 10,
          "equipment_count": 5,
          "utilization_factor": 0.80
        },
        "test_capabilities": [
          {
            "test_type_id": "uuid",
            "is_available": true,
            "time_per_test_minutes": 180,
            "staff_required": 2,
            "equipment_utilization": 0.5,
            "cost_per_test": 25.00,
            "quality_score": 0.95
          }
        ]
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 50,
      "total": 15,
      "pages": 1
    }
  }
}
```

### POST /networks/{network_id}/laboratories
Create new laboratory.

**Request Body:**
```json
{
  "laboratory_id": "LAB001",
  "name": "Central Laboratory",
  "coordinates": {
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "address": "123 Main St, City, State",
  "phone": "+1-555-0123",
  "email": "lab@example.com",
  "operational_hours": {
    "monday": {
      "open_time": "08:00",
      "close_time": "17:00",
      "is_closed": false
    }
  },
  "capacities": {
    "max_tests_per_day": 100,
    "max_tests_per_month": 2500,
    "staff_count": 10,
    "equipment_count": 5,
    "utilization_factor": 0.80
  },
  "test_capabilities": [
    {
      "test_type_id": "uuid",
      "is_available": true,
      "time_per_test_minutes": 180,
      "staff_required": 2,
      "equipment_utilization": 0.5,
      "cost_per_test": 25.00,
      "quality_score": 0.95
    }
  ]
}
```

### GET /laboratories/{laboratory_id}
Get laboratory details.

### PUT /laboratories/{laboratory_id}
Update laboratory.

### DELETE /laboratories/{laboratory_id}
Delete laboratory.

---

## 5. Test Type Endpoints

### GET /test-types
List all test types.

**Response:**
```json
{
  "success": true,
  "data": {
    "test_types": [
      {
        "id": "uuid",
        "name": "Culture Test - Basic",
        "description": "Basic bacterial culture identification",
        "category": "culture",
        "standard_duration_minutes": 180,
        "complexity_level": 2,
        "created_at": "2024-01-01T12:00:00Z"
      }
    ]
  }
}
```

### POST /test-types
Create new test type (Admin only).

### GET /test-types/{test_type_id}
Get test type details.

### PUT /test-types/{test_type_id}
Update test type (Admin only).

### DELETE /test-types/{test_type_id}
Delete test type (Admin only).

---

## 6. Service Area Endpoints

### GET /networks/{network_id}/service-areas
List service areas in network.

**Query Parameters:**
- `page` (integer, default: 1)
- `limit` (integer, default: 50)
- `search` (string, optional)
- `bbox` (string, optional): Bounding box filter
- `min_population` (integer, optional)

### POST /networks/{network_id}/service-areas
Create new service area.

**Request Body:**
```json
{
  "area_id": "AREA001",
  "name": "Downtown District",
  "coordinates": {
    "latitude": 40.7589,
    "longitude": -73.9851
  },
  "population": 50000
}
```

### GET /service-areas/{area_id}
Get service area details.

### PUT /service-areas/{area_id}
Update service area.

### DELETE /service-areas/{area_id}
Delete service area.

---

## 7. Test Demand Endpoints

### GET /service-areas/{area_id}/demand
Get test demand for service area.

**Query Parameters:**
- `start_date` (date, optional)
- `end_date` (date, optional)
- `test_type_id` (uuid, optional)

### POST /service-areas/{area_id}/demand
Create test demand record.

**Request Body:**
```json
{
  "test_type_id": "uuid",
  "demand_date": "2024-01-01",
  "test_count": 50,
  "priority_level": 3
}
```

### PUT /demand/{demand_id}
Update test demand.

### DELETE /demand/{demand_id}
Delete test demand.

---

## 8. Optimization Endpoints

### GET /networks/{network_id}/scenarios
List optimization scenarios.

**Query Parameters:**
- `page` (integer, default: 1)
- `limit` (integer, default: 20)
- `status` (string, optional): Filter by status

**Response:**
```json
{
  "success": true,
  "data": {
    "scenarios": [
      {
        "id": "uuid",
        "name": "Scenario 1: Cost Optimization",
        "description": "Focus on reducing transportation costs",
        "status": "completed",
        "created_by": "uuid",
        "started_at": "2024-01-01T10:00:00Z",
        "completed_at": "2024-01-01T10:15:00Z",
        "execution_time_seconds": 900,
        "created_at": "2024-01-01T09:00:00Z",
        "parameters": {
          "weights": {
            "distance": 0.20,
            "time": 0.15,
            "cost": 0.35,
            "utilization": 0.20,
            "accessibility": 0.10
          }
        }
      }
    ]
  }
}
```

### POST /networks/{network_id}/scenarios
Create optimization scenario.

**Request Body:**
```json
{
  "name": "Cost Optimization Scenario",
  "description": "Optimize for minimum transportation costs",
  "parameters": {
    "weights": {
      "distance": 0.20,
      "time": 0.15,
      "cost": 0.35,
      "utilization": 0.20,
      "accessibility": 0.10
    },
    "constraints": {
      "max_distance_km": 50,
      "max_travel_time_minutes": 120,
      "min_utilization_rate": 0.3,
      "max_utilization_rate": 0.9,
      "enforce_operational_hours": true,
      "quality_threshold": 0.7
    },
    "algorithm_config": {
      "population_size": 200,
      "max_generations": 500,
      "crossover_rate": 0.9,
      "mutation_rate": 0.05,
      "convergence_threshold": 0.001
    }
  }
}
```

### GET /scenarios/{scenario_id}
Get scenario details and status.

### POST /scenarios/{scenario_id}/run
Execute optimization scenario.

**Response:**
```json
{
  "success": true,
  "data": {
    "scenario_id": "uuid",
    "status": "running",
    "estimated_completion": "2024-01-01T10:15:00Z",
    "progress": 0
  }
}
```

### GET /scenarios/{scenario_id}/status
Get optimization status and progress.

**Response:**
```json
{
  "success": true,
  "data": {
    "scenario_id": "uuid",
    "status": "running",
    "progress": 65,
    "current_generation": 325,
    "max_generations": 500,
    "best_fitness": 0.85,
    "estimated_completion": "2024-01-01T10:15:00Z"
  }
}
```

### POST /scenarios/{scenario_id}/cancel
Cancel running optimization.

### DELETE /scenarios/{scenario_id}
Delete optimization scenario.

---

## 9. Optimization Results Endpoints

### GET /scenarios/{scenario_id}/results
Get optimization results.

**Query Parameters:**
- `page` (integer, default: 1)
- `limit` (integer, default: 100)
- `laboratory_id` (uuid, optional)
- `service_area_id` (uuid, optional)
- `test_type_id` (uuid, optional)

**Response:**
```json
{
  "success": true,
  "data": {
    "scenario_id": "uuid",
    "status": "completed",
    "summary": {
      "total_allocations": 1500,
      "average_distance_reduction": 15.2,
      "cost_savings_percentage": 12.8,
      "utilization_improvement": 8.5,
      "accessibility_improvement": 5.3,
      "execution_time_seconds": 900
    },
    "results": [
      {
        "id": "uuid",
        "service_area_id": "uuid",
        "laboratory_id": "uuid",
        "test_type_id": "uuid",
        "allocated_tests": 25,
        "distance_km": 8.5,
        "travel_time_minutes": 15,
        "transport_cost": 12.50,
        "processing_cost": 625.00,
        "total_cost": 637.50,
        "utilization_score": 0.75,
        "accessibility_score": 0.90
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 100,
      "total": 1500,
      "pages": 15
    }
  }
}
```

### GET /scenarios/{scenario_id}/comparison
Compare optimization results with current allocations.

### GET /scenarios/{scenario_id}/export
Export results in various formats.

**Query Parameters:**
- `format` (string): "csv", "excel", "json", "pdf"
- `include_maps` (boolean, default: true)
- `include_statistics` (boolean, default: true)

---

## 10. Routing and Distance Endpoints

### POST /routing/distance
Calculate distance and travel time between points.

**Request Body:**
```json
{
  "origin": {
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "destination": {
    "latitude": 40.7589,
    "longitude": -73.9851
  },
  "provider": "osrm"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "distance_km": 8.5,
    "duration_minutes": 15,
    "provider": "osrm",
    "route_geometry": "encoded_polyline_string",
    "cached": false
  }
}
```

### POST /routing/batch
Calculate distances for multiple origin-destination pairs.

**Request Body:**
```json
{
  "pairs": [
    {
      "origin": {"latitude": 40.7128, "longitude": -74.0060},
      "destination": {"latitude": 40.7589, "longitude": -73.9851}
    }
  ],
  "provider": "osrm"
}
```

---

## 11. File Upload and Data Import Endpoints

### POST /upload
Upload data files for processing.

**Request:** Multipart form data
- `file`: File to upload (CSV, Excel, JSON)
- `type`: Data type ("laboratories", "service_areas", "test_demand")
- `network_id`: Target network UUID

**Response:**
```json
{
  "success": true,
  "data": {
    "upload_id": "uuid",
    "filename": "laboratories.csv",
    "size": 1024000,
    "content_type": "text/csv",
    "status": "processing",
    "message": "File uploaded successfully, processing started"
  }
}
```

### GET /upload/{upload_id}/status
Get upload processing status.

**Response:**
```json
{
  "success": true,
  "data": {
    "upload_id": "uuid",
    "status": "completed",
    "total_rows": 100,
    "processed_rows": 100,
    "successful_rows": 95,
    "failed_rows": 5,
    "errors": [
      {
        "row": 15,
        "column": "latitude",
        "value": "invalid",
        "message": "Invalid latitude value"
      }
    ],
    "warnings": [
      "Some optional fields were empty and filled with defaults"
    ]
  }
}
```

### GET /templates/{type}
Download data import templates.

**Path Parameters:**
- `type`: "laboratories", "service_areas", "test_demand"

**Query Parameters:**
- `format`: "csv", "excel" (default: "csv")

---

## 12. Analytics and Reporting Endpoints

### GET /networks/{network_id}/analytics
Get network analytics dashboard data.

**Response:**
```json
{
  "success": true,
  "data": {
    "overview": {
      "total_laboratories": 15,
      "total_service_areas": 25,
      "total_monthly_capacity": 5000,
      "current_utilization": 0.75,
      "coverage_percentage": 85.2
    },
    "utilization_by_lab": [
      {
        "laboratory_id": "uuid",
        "name": "Central Lab",
        "utilization": 0.85,
        "capacity": 500
      }
    ],
    "distance_distribution": {
      "bins": ["0-5km", "5-10km", "10-20km", "20+km"],
      "counts": [150, 300, 200, 50]
    },
    "cost_analysis": {
      "total_monthly_cost": 125000,
      "cost_per_test": 25.50,
      "transport_cost_percentage": 15.2
    }
  }
}
```

### GET /scenarios/{scenario_id}/report
Generate comprehensive optimization report.

**Query Parameters:**
- `format`: "html", "pdf" (default: "html")
- `include_maps`: boolean (default: true)
- `include_recommendations`: boolean (default: true)

---

## 13. System Management Endpoints

### GET /health
System health check (no authentication required).

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00Z",
    "version": "1.0.0",
    "database": true,
    "routing_api": true,
    "optimization_engine": true,
    "cache": true
  }
}
```

### GET /config
Get system configuration (Admin only).

### PUT /config
Update system configuration (Admin only).

**Request Body:**
```json
{
  "key": "optimization_weights",
  "value": {
    "distance": 0.25,
    "time": 0.20,
    "cost": 0.25,
    "utilization": 0.20,
    "accessibility": 0.10
  },
  "description": "Default optimization weights"
}
```

---

## Error Handling

### Common Error Codes

- `VALIDATION_ERROR`: Request validation failed
- `AUTHENTICATION_REQUIRED`: Missing or invalid authentication
- `PERMISSION_DENIED`: Insufficient permissions
- `RESOURCE_NOT_FOUND`: Requested resource not found
- `RESOURCE_CONFLICT`: Resource already exists or conflict
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `OPTIMIZATION_FAILED`: Optimization algorithm failed
- `FILE_PROCESSING_ERROR`: File upload/processing error
- `EXTERNAL_API_ERROR`: External service unavailable

### Rate Limiting

- Authentication endpoints: 5 requests per minute
- File upload endpoints: 10 requests per hour
- Optimization endpoints: 3 concurrent optimizations per user
- General API endpoints: 1000 requests per hour per user

### Pagination

All list endpoints support pagination with the following parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

Response includes pagination metadata:
```json
{
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```