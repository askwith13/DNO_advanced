"""
Laboratory Network model representing a collection of laboratories and service areas.
Manages the network configuration for optimization scenarios.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
import enum

from app.models.base import BaseModel, AuditMixin


class NetworkStatus(str, enum.Enum):
    """Network status options."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"
    ARCHIVED = "archived"


class LaboratoryNetwork(BaseModel, AuditMixin):
    """Laboratory network containing multiple laboratories and service areas."""
    
    __tablename__ = "laboratory_networks"
    
    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), default=NetworkStatus.ACTIVE.value, nullable=False)
    
    # Geographic Information
    region = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    state_province = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    
    # Network Metrics (calculated fields)
    total_laboratories = Column(Integer, default=0, nullable=False)
    total_service_areas = Column(Integer, default=0, nullable=False)
    total_capacity_per_day = Column(Integer, default=0, nullable=False)
    total_capacity_per_month = Column(Integer, default=0, nullable=False)
    
    # Geographic Coverage
    coverage_area_km2 = Column(Float, nullable=True)
    center_latitude = Column(Float, nullable=True)
    center_longitude = Column(Float, nullable=True)
    bounding_box = Column(Geography('POLYGON'), nullable=True)
    
    # Network Configuration
    default_max_distance_km = Column(Float, default=50.0, nullable=False)
    default_max_travel_time_minutes = Column(Integer, default=90, nullable=False)
    
    # Management
    manager_id = Column(String, ForeignKey("users.id"), nullable=True)
    manager = relationship("User", back_populates="managed_networks")
    
    # Relationships
    laboratories = relationship(
        "Laboratory", 
        back_populates="network", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    service_areas = relationship(
        "ServiceArea", 
        back_populates="network", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    optimization_scenarios = relationship(
        "OptimizationScenario", 
        back_populates="network", 
        cascade="all, delete-orphan"
    )
    
    test_demand_records = relationship(
        "TestDemand", 
        back_populates="network", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<LaboratoryNetwork(name='{self.name}', laboratories={self.total_laboratories})>"
    
    def calculate_network_metrics(self) -> None:
        """Calculate and update network metrics."""
        # Count laboratories and service areas
        self.total_laboratories = self.laboratories.filter_by(is_active=True).count()
        self.total_service_areas = self.service_areas.filter_by(is_active=True).count()
        
        # Calculate total capacity
        active_labs = self.laboratories.filter_by(is_active=True).all()
        self.total_capacity_per_day = sum(lab.max_tests_per_day or 0 for lab in active_labs)
        self.total_capacity_per_month = sum(lab.max_tests_per_month or 0 for lab in active_labs)
        
        # Calculate geographic center and coverage
        if active_labs:
            latitudes = [lab.latitude for lab in active_labs if lab.latitude]
            longitudes = [lab.longitude for lab in active_labs if lab.longitude]
            
            if latitudes and longitudes:
                self.center_latitude = sum(latitudes) / len(latitudes)
                self.center_longitude = sum(longitudes) / len(longitudes)
                
                # Calculate approximate coverage area (simplified)
                lat_range = max(latitudes) - min(latitudes)
                lon_range = max(longitudes) - min(longitudes)
                # Rough approximation: 1 degree ≈ 111 km
                self.coverage_area_km2 = lat_range * lon_range * 111 * 111
    
    def get_active_laboratories(self):
        """Get all active laboratories in the network."""
        return self.laboratories.filter_by(is_active=True).all()
    
    def get_active_service_areas(self):
        """Get all active service areas in the network."""
        return self.service_areas.filter_by(is_active=True).all()
    
    def get_utilization_rate(self) -> float:
        """Calculate current network utilization rate."""
        if self.total_capacity_per_day == 0:
            return 0.0
        
        # Get current test demand
        from app.models.test_demand import TestDemand
        from sqlalchemy import func
        
        current_demand = (
            TestDemand.query
            .filter_by(network_id=self.id, is_active=True)
            .with_entities(func.sum(TestDemand.test_count))
            .scalar() or 0
        )
        
        return min(current_demand / self.total_capacity_per_day, 1.0)
    
    def get_network_summary(self) -> dict:
        """Get comprehensive network summary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "region": self.region,
            "country": self.country,
            "total_laboratories": self.total_laboratories,
            "total_service_areas": self.total_service_areas,
            "total_capacity_per_day": self.total_capacity_per_day,
            "total_capacity_per_month": self.total_capacity_per_month,
            "coverage_area_km2": self.coverage_area_km2,
            "center_coordinates": {
                "latitude": self.center_latitude,
                "longitude": self.center_longitude
            } if self.center_latitude and self.center_longitude else None,
            "utilization_rate": self.get_utilization_rate(),
            "manager": {
                "id": self.manager.id,
                "name": self.manager.full_name,
                "email": self.manager.email
            } if self.manager else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    def validate_network_configuration(self) -> List[str]:
        """Validate network configuration and return list of issues."""
        issues = []
        
        # Check minimum requirements
        if self.total_laboratories < 1:
            issues.append("Network must have at least one laboratory")
        
        if self.total_service_areas < 1:
            issues.append("Network must have at least one service area")
        
        # Check geographic configuration
        active_labs = self.get_active_laboratories()
        if active_labs:
            labs_with_coords = [lab for lab in active_labs if lab.latitude and lab.longitude]
            if len(labs_with_coords) != len(active_labs):
                issues.append("All laboratories must have valid coordinates")
        
        # Check capacity configuration
        labs_without_capacity = [lab for lab in active_labs if not lab.max_tests_per_day]
        if labs_without_capacity:
            issues.append(f"{len(labs_without_capacity)} laboratories missing capacity information")
        
        # Check service area coverage
        active_areas = self.get_active_service_areas()
        if active_areas:
            areas_with_coords = [area for area in active_areas if area.latitude and area.longitude]
            if len(areas_with_coords) != len(active_areas):
                issues.append("All service areas must have valid coordinates")
        
        return issues
    
    def is_ready_for_optimization(self) -> bool:
        """Check if network is ready for optimization."""
        issues = self.validate_network_configuration()
        return len(issues) == 0
    
    def get_optimization_constraints(self) -> dict:
        """Get default optimization constraints for this network."""
        return {
            "max_distance_km": self.default_max_distance_km,
            "max_travel_time_minutes": self.default_max_travel_time_minutes,
            "enforce_laboratory_hours": True,
            "min_utilization_rate": 0.3,
            "max_utilization_rate": 0.9,
            "quality_threshold": 0.7,
        }
    
    def export_network_data(self) -> dict:
        """Export complete network data for optimization or backup."""
        return {
            "network": self.get_network_summary(),
            "laboratories": [lab.to_dict() for lab in self.get_active_laboratories()],
            "service_areas": [area.to_dict() for area in self.get_active_service_areas()],
            "test_demand": [
                demand.to_dict() 
                for demand in self.test_demand_records.filter_by(is_active=True).all()
            ],
        }
    
    @classmethod
    def create_network_from_template(cls, template_name: str, **kwargs) -> "LaboratoryNetwork":
        """Create network from predefined template."""
        templates = {
            "urban_network": {
                "default_max_distance_km": 25.0,
                "default_max_travel_time_minutes": 60,
                "description": "Urban laboratory network template with shorter distances"
            },
            "rural_network": {
                "default_max_distance_km": 100.0,
                "default_max_travel_time_minutes": 180,
                "description": "Rural laboratory network template with longer distances"
            },
            "regional_network": {
                "default_max_distance_km": 50.0,
                "default_max_travel_time_minutes": 90,
                "description": "Regional laboratory network template with moderate distances"
            }
        }
        
        template_config = templates.get(template_name, templates["regional_network"])
        template_config.update(kwargs)
        
        return cls(**template_config)