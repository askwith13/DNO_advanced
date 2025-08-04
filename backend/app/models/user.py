"""
User model with authentication and role-based access control.
Supports multiple user types: Network Analyst, Laboratory Manager, Healthcare Planner, System Administrator.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Integer, Text, func
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
import enum

from app.models.base import BaseModel, UUIDMixin, AuditMixin

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(str, enum.Enum):
    """User roles with specific permissions."""
    NETWORK_ANALYST = "network_analyst"
    LABORATORY_MANAGER = "laboratory_manager"
    HEALTHCARE_PLANNER = "healthcare_planner"
    SYSTEM_ADMINISTRATOR = "system_administrator"


class UserStatus(str, enum.Enum):
    """User account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"
    PENDING = "pending"


class User(BaseModel, UUIDMixin, AuditMixin):
    """User model with authentication and authorization."""
    
    __tablename__ = "users"
    
    # Basic Information
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Role and Permissions
    role = Column(Enum(UserRole), nullable=False, default=UserRole.NETWORK_ANALYST)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    
    # Profile Information
    phone = Column(String(50), nullable=True)
    organization = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Authentication
    last_login = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    password_changed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Account Settings
    email_verified = Column(Boolean, default=False, nullable=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    
    # Preferences
    timezone = Column(String(50), default="UTC", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    theme = Column(String(20), default="light", nullable=False)
    
    # Relationships
    # User can manage multiple laboratory networks (for Laboratory Managers)
    managed_networks = relationship("LaboratoryNetwork", back_populates="manager")
    
    # User can create optimization scenarios
    optimization_scenarios = relationship("OptimizationScenario", back_populates="created_by_user")
    
    # Audit trail
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(email='{self.email}', role='{self.role}')>"
    
    @classmethod
    def create_user(
        cls,
        email: str,
        password: str,
        full_name: str,
        role: UserRole = UserRole.NETWORK_ANALYST,
        **kwargs
    ) -> "User":
        """Create a new user with hashed password."""
        hashed_password = pwd_context.hash(password)
        
        user = cls(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            **kwargs
        )
        
        return user
    
    def verify_password(self, password: str) -> bool:
        """Verify user password."""
        return pwd_context.verify(password, self.hashed_password)
    
    def set_password(self, password: str) -> None:
        """Set new password for user."""
        self.hashed_password = pwd_context.hash(password)
        self.password_changed_at = datetime.utcnow()
        self.failed_login_attempts = 0
        self.locked_until = None
    
    def is_active_user(self) -> bool:
        """Check if user account is active."""
        return (
            self.status == UserStatus.ACTIVE and
            self.is_active and
            (self.locked_until is None or self.locked_until < datetime.utcnow())
        )
    
    def is_locked(self) -> bool:
        """Check if user account is locked."""
        return (
            self.status == UserStatus.LOCKED or
            (self.locked_until is not None and self.locked_until > datetime.utcnow())
        )
    
    def increment_failed_login(self, max_attempts: int = 5, lockout_duration: int = 900) -> None:
        """Increment failed login attempts and lock account if necessary."""
        self.failed_login_attempts += 1
        
        if self.failed_login_attempts >= max_attempts:
            self.locked_until = datetime.utcnow() + datetime.timedelta(seconds=lockout_duration)
            self.status = UserStatus.LOCKED
    
    def reset_failed_login(self) -> None:
        """Reset failed login attempts after successful login."""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login = datetime.utcnow()
        
        if self.status == UserStatus.LOCKED:
            self.status = UserStatus.ACTIVE
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission based on role."""
        permissions = {
            UserRole.SYSTEM_ADMINISTRATOR: [
                "user.create", "user.read", "user.update", "user.delete",
                "network.create", "network.read", "network.update", "network.delete",
                "laboratory.create", "laboratory.read", "laboratory.update", "laboratory.delete",
                "optimization.create", "optimization.read", "optimization.update", "optimization.delete",
                "system.admin", "audit.read", "reports.all"
            ],
            UserRole.NETWORK_ANALYST: [
                "network.create", "network.read", "network.update",
                "laboratory.create", "laboratory.read", "laboratory.update",
                "optimization.create", "optimization.read", "optimization.update", "optimization.delete",
                "data.import", "data.export", "reports.technical"
            ],
            UserRole.LABORATORY_MANAGER: [
                "network.read", "laboratory.read", "laboratory.update",
                "optimization.read", "reports.laboratory"
            ],
            UserRole.HEALTHCARE_PLANNER: [
                "network.read", "optimization.read", "reports.executive"
            ]
        }
        
        return permission in permissions.get(self.role, [])
    
    def can_access_network(self, network_id: int) -> bool:
        """Check if user can access specific network."""
        if self.role == UserRole.SYSTEM_ADMINISTRATOR:
            return True
        
        if self.role == UserRole.LABORATORY_MANAGER:
            # Laboratory managers can only access networks they manage
            return any(network.id == network_id for network in self.managed_networks)
        
        # Network analysts and healthcare planners can access all networks
        return self.role in [UserRole.NETWORK_ANALYST, UserRole.HEALTHCARE_PLANNER]
    
    def get_accessible_networks(self):
        """Get list of networks user can access."""
        if self.role == UserRole.SYSTEM_ADMINISTRATOR:
            # Import here to avoid circular imports
            from app.models.network import LaboratoryNetwork
            return LaboratoryNetwork.query.all()
        
        if self.role == UserRole.LABORATORY_MANAGER:
            return self.managed_networks
        
        # Network analysts and healthcare planners can access all networks
        from app.models.network import LaboratoryNetwork
        return LaboratoryNetwork.query.filter_by(is_active=True).all()
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Convert user to dictionary, optionally including sensitive data."""
        data = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "role": self.role.value,
            "status": self.status.value,
            "phone": self.phone,
            "organization": self.organization,
            "department": self.department,
            "title": self.title,
            "bio": self.bio,
            "last_login": self.last_login,
            "email_verified": self.email_verified,
            "two_factor_enabled": self.two_factor_enabled,
            "timezone": self.timezone,
            "language": self.language,
            "theme": self.theme,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
        }
        
        if include_sensitive:
            data.update({
                "failed_login_attempts": self.failed_login_attempts,
                "locked_until": self.locked_until,
                "password_changed_at": self.password_changed_at,
            })
        
        return data


class UserSession(BaseModel):
    """User session tracking for security and audit purposes."""
    
    __tablename__ = "user_sessions"
    
    user_id = Column(String, nullable=False, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    refresh_token = Column(String(255), unique=True, nullable=True, index=True)
    
    # Session metadata
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(Text, nullable=True)
    device_fingerprint = Column(String(255), nullable=True)
    
    # Session status
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    
    # Location data (optional)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    
    def __repr__(self) -> str:
        return f"<UserSession(user_id='{self.user_id}', active='{self.is_active}')>"
    
    def is_expired(self) -> bool:
        """Check if session is expired."""
        return datetime.utcnow() > self.expires_at
    
    def extend_session(self, minutes: int = 60) -> None:
        """Extend session expiration time."""
        self.expires_at = datetime.utcnow() + datetime.timedelta(minutes=minutes)
        self.last_activity = datetime.utcnow()
    
    def invalidate(self) -> None:
        """Invalidate the session."""
        self.is_active = False