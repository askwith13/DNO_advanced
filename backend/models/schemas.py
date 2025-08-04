"""
Pydantic Data Models for CDST Diagnostic Network Optimization Platform
"""

from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Dict, Any, Union
from uuid import UUID

from pydantic import BaseModel, Field, validator, EmailStr
from geojson_pydantic import Point


# Enums
class UserRole(str, Enum):
    ADMINISTRATOR = "administrator"
    ANALYST = "analyst"
    VIEWER = "viewer"


class OptimizationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TestCategory(str, Enum):
    CULTURE = "culture"
    SENSITIVITY = "sensitivity"
    SPECIALIZED = "specialized"
    RAPID = "rapid"


class RoutingProvider(str, Enum):
    OSRM = "osrm"
    HAVERSINE = "haversine"


# Base Models
class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            Decimal: lambda d: float(d),
        }


# User Management Models
class UserBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    organization: Optional[str] = Field(None, max_length=255)
    role: UserRole


class UserCreate(UserBase):
    password: str = Field(..., min_length=12, max_length=255)

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    organization: Optional[str] = Field(None, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None


# Authentication Models
class LoginRequest(BaseSchema):
    username: str
    password: str


class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# Coordinate Models
class Coordinates(BaseSchema):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @validator('latitude')
    def validate_latitude(cls, v):
        return round(v, 8)  # 6-8 decimal places for GPS precision

    @validator('longitude')
    def validate_longitude(cls, v):
        return round(v, 8)


# Laboratory Network Models
class LaboratoryNetworkBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class LaboratoryNetworkCreate(LaboratoryNetworkBase):
    pass


class LaboratoryNetworkUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class LaboratoryNetworkResponse(LaboratoryNetworkBase):
    id: UUID
    created_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool


# Operational Hours Models
class OperationalHours(BaseSchema):
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    is_closed: bool = False

    @validator('close_time')
    def validate_close_time(cls, v, values):
        if v and values.get('open_time') and v <= values['open_time']:
            raise ValueError('Close time must be after open time')
        return v


class WeeklyHours(BaseSchema):
    monday: Optional[OperationalHours] = None
    tuesday: Optional[OperationalHours] = None
    wednesday: Optional[OperationalHours] = None
    thursday: Optional[OperationalHours] = None
    friday: Optional[OperationalHours] = None
    saturday: Optional[OperationalHours] = None
    sunday: Optional[OperationalHours] = None


# Laboratory Models
class LaboratoryCapacities(BaseSchema):
    max_tests_per_day: int = Field(..., gt=0)
    max_tests_per_month: int = Field(..., gt=0)
    staff_count: int = Field(..., gt=0)
    equipment_count: int = Field(1, gt=0)
    utilization_factor: float = Field(0.80, ge=0, le=1)

    @validator('max_tests_per_month')
    def validate_monthly_capacity(cls, v, values):
        daily = values.get('max_tests_per_day')
        if daily and v < daily:
            raise ValueError('Monthly capacity must be at least equal to daily capacity')
        return v


class TestCapability(BaseSchema):
    test_type_id: UUID
    is_available: bool = True
    time_per_test_minutes: int = Field(..., gt=0, le=1440)  # Max 24 hours
    staff_required: int = Field(1, gt=0)
    equipment_utilization: float = Field(0.50, ge=0, le=1)
    cost_per_test: float = Field(0.00, ge=0)
    quality_score: float = Field(1.00, ge=0, le=1)


class LaboratoryBase(BaseSchema):
    laboratory_id: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    coordinates: Coordinates
    address: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None


class LaboratoryCreate(LaboratoryBase):
    network_id: UUID
    operational_hours: Optional[WeeklyHours] = None
    capacities: LaboratoryCapacities
    test_capabilities: List[TestCapability] = []


class LaboratoryUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    coordinates: Optional[Coordinates] = None
    address: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    operational_hours: Optional[WeeklyHours] = None
    capacities: Optional[LaboratoryCapacities] = None
    test_capabilities: Optional[List[TestCapability]] = None


class LaboratoryResponse(LaboratoryBase):
    id: UUID
    network_id: UUID
    created_at: datetime
    updated_at: datetime
    operational_hours: Optional[WeeklyHours] = None
    capacities: Optional[LaboratoryCapacities] = None
    test_capabilities: List[TestCapability] = []


# Test Type Models
class TestTypeBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: TestCategory
    standard_duration_minutes: int = Field(..., gt=0)
    complexity_level: int = Field(1, ge=1, le=5)


class TestTypeCreate(TestTypeBase):
    pass


class TestTypeUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[TestCategory] = None
    standard_duration_minutes: Optional[int] = Field(None, gt=0)
    complexity_level: Optional[int] = Field(None, ge=1, le=5)


class TestTypeResponse(TestTypeBase):
    id: UUID
    created_at: datetime


# Service Area Models
class ServiceAreaBase(BaseSchema):
    area_id: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    coordinates: Coordinates
    population: int = Field(0, ge=0)


class ServiceAreaCreate(ServiceAreaBase):
    network_id: UUID


class ServiceAreaUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    coordinates: Optional[Coordinates] = None
    population: Optional[int] = Field(None, ge=0)


class ServiceAreaResponse(ServiceAreaBase):
    id: UUID
    network_id: UUID
    created_at: datetime


# Test Demand Models
class TestDemandBase(BaseSchema):
    test_type_id: UUID
    demand_date: date
    test_count: int = Field(..., ge=0)
    priority_level: int = Field(1, ge=1, le=5)


class TestDemandCreate(TestDemandBase):
    service_area_id: UUID


class TestDemandUpdate(BaseSchema):
    test_count: Optional[int] = Field(None, ge=0)
    priority_level: Optional[int] = Field(None, ge=1, le=5)


class TestDemandResponse(TestDemandBase):
    id: UUID
    service_area_id: UUID
    created_at: datetime


# Optimization Models
class OptimizationWeights(BaseSchema):
    distance: float = Field(0.25, ge=0, le=1)
    time: float = Field(0.20, ge=0, le=1)
    cost: float = Field(0.25, ge=0, le=1)
    utilization: float = Field(0.20, ge=0, le=1)
    accessibility: float = Field(0.10, ge=0, le=1)

    @validator('accessibility')
    def validate_weights_sum(cls, v, values):
        total = v + values.get('distance', 0) + values.get('time', 0) + \
                values.get('cost', 0) + values.get('utilization', 0)
        if abs(total - 1.0) > 0.001:  # Allow small floating point errors
            raise ValueError('Optimization weights must sum to 1.0')
        return v


class OptimizationConstraints(BaseSchema):
    max_distance_km: Optional[float] = Field(None, gt=0)
    max_travel_time_minutes: Optional[int] = Field(None, gt=0)
    min_utilization_rate: float = Field(0.0, ge=0, le=1)
    max_utilization_rate: float = Field(1.0, ge=0, le=1)
    enforce_operational_hours: bool = True
    quality_threshold: float = Field(0.0, ge=0, le=1)


class OptimizationParameters(BaseSchema):
    weights: OptimizationWeights
    constraints: OptimizationConstraints
    algorithm_config: Dict[str, Any] = {
        "population_size": 200,
        "max_generations": 500,
        "crossover_rate": 0.9,
        "mutation_rate": 0.05,
        "convergence_threshold": 0.001
    }


class OptimizationScenarioBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    parameters: OptimizationParameters


class OptimizationScenarioCreate(OptimizationScenarioBase):
    network_id: UUID


class OptimizationScenarioUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    parameters: Optional[OptimizationParameters] = None


class OptimizationScenarioResponse(OptimizationScenarioBase):
    id: UUID
    network_id: UUID
    created_by: Optional[UUID] = None
    status: OptimizationStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time_seconds: Optional[int] = None
    created_at: datetime
    updated_at: datetime


# Optimization Results Models
class OptimizationResultBase(BaseSchema):
    allocated_tests: int = Field(..., ge=0)
    distance_km: Optional[float] = Field(None, ge=0)
    travel_time_minutes: Optional[int] = Field(None, ge=0)
    transport_cost: Optional[float] = Field(None, ge=0)
    processing_cost: Optional[float] = Field(None, ge=0)
    total_cost: Optional[float] = Field(None, ge=0)
    utilization_score: Optional[float] = Field(None, ge=0, le=1)
    accessibility_score: Optional[float] = Field(None, ge=0, le=1)


class OptimizationResultCreate(OptimizationResultBase):
    scenario_id: UUID
    service_area_id: UUID
    laboratory_id: UUID
    test_type_id: UUID


class OptimizationResultResponse(OptimizationResultBase):
    id: UUID
    scenario_id: UUID
    service_area_id: UUID
    laboratory_id: UUID
    test_type_id: UUID
    created_at: datetime


# File Upload Models
class FileUploadResponse(BaseSchema):
    filename: str
    size: int
    content_type: str
    upload_id: UUID
    status: str
    message: Optional[str] = None
    errors: List[str] = []


class ValidationError(BaseSchema):
    row: int
    column: str
    value: Any
    message: str


class DataValidationResult(BaseSchema):
    is_valid: bool
    total_rows: int
    valid_rows: int
    errors: List[ValidationError] = []
    warnings: List[str] = []


# Route and Distance Models
class RouteRequest(BaseSchema):
    origin: Coordinates
    destination: Coordinates
    provider: RoutingProvider = RoutingProvider.OSRM


class RouteResponse(BaseSchema):
    distance_km: float
    duration_minutes: int
    provider: RoutingProvider
    route_geometry: Optional[str] = None
    cached: bool = False


# Analytics and Reporting Models
class NetworkStatistics(BaseSchema):
    total_laboratories: int
    total_service_areas: int
    total_test_types: int
    average_distance_km: float
    average_utilization: float
    total_monthly_capacity: int
    coverage_percentage: float


class OptimizationSummary(BaseSchema):
    scenario_id: UUID
    total_allocations: int
    average_distance_reduction: float
    cost_savings_percentage: float
    utilization_improvement: float
    accessibility_improvement: float
    execution_time_seconds: int


class ReportRequest(BaseSchema):
    scenario_id: UUID
    format: str = Field("html", regex="^(html|pdf|excel|csv)$")
    include_maps: bool = True
    include_statistics: bool = True
    include_recommendations: bool = True


# Bulk Operations Models
class BulkOperationStatus(BaseSchema):
    operation_id: UUID
    status: str
    total_items: int
    processed_items: int
    successful_items: int
    failed_items: int
    errors: List[str] = []
    started_at: datetime
    completed_at: Optional[datetime] = None


# System Configuration Models
class SystemConfigUpdate(BaseSchema):
    key: str
    value: Dict[str, Any]
    description: Optional[str] = None


class SystemConfigResponse(BaseSchema):
    id: UUID
    key: str
    value: Dict[str, Any]
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# Health Check Models
class HealthCheckResponse(BaseSchema):
    status: str
    timestamp: datetime
    version: str
    database: bool
    routing_api: bool
    optimization_engine: bool
    cache: bool