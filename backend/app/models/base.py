"""
Base model class with common fields and utilities.
All database models inherit from this base class.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Column, DateTime, Integer, String, Boolean, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session
import uuid


@as_declarative()
class Base:
    """Base class for all database models."""
    
    id: Any
    __name__: str
    
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseModel(Base):
    """Base model with common audit fields."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update model instance from dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @classmethod
    def create(cls, db: Session, **kwargs) -> "BaseModel":
        """Create a new instance of the model."""
        instance = cls(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
    
    def update(self, db: Session, **kwargs) -> "BaseModel":
        """Update the model instance."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(self)
        return self
    
    def delete(self, db: Session, soft_delete: bool = True) -> None:
        """Delete the model instance (soft delete by default)."""
        if soft_delete:
            self.is_active = False
            self.updated_at = datetime.utcnow()
            db.commit()
        else:
            db.delete(self)
            db.commit()


class UUIDMixin:
    """Mixin for models that use UUID as primary key."""
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)


class TimestampMixin:
    """Mixin for models that need timestamp tracking."""
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class SoftDeleteMixin:
    """Mixin for models that support soft deletion."""
    
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def soft_delete(self, db: Session) -> None:
        """Perform soft delete on the instance."""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        db.commit()
    
    def restore(self, db: Session) -> None:
        """Restore a soft-deleted instance."""
        self.is_deleted = False
        self.deleted_at = None
        db.commit()


class AuditMixin:
    """Mixin for models that need audit trail."""
    
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
    version = Column(Integer, default=1, nullable=False)
    
    def increment_version(self) -> None:
        """Increment the version number."""
        self.version += 1


# Utility functions for model operations
def get_or_create(db: Session, model_class, defaults: Optional[Dict] = None, **kwargs):
    """Get existing instance or create new one."""
    instance = db.query(model_class).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items())
        params.update(defaults or {})
        instance = model_class(**params)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance, True


def bulk_create(db: Session, model_class, data_list: list) -> list:
    """Create multiple instances efficiently."""
    instances = []
    for data in data_list:
        instance = model_class(**data)
        instances.append(instance)
    
    db.bulk_save_objects(instances)
    db.commit()
    return instances


def paginate_query(query, page: int = 1, per_page: int = 20):
    """Add pagination to a query."""
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page,
        'has_prev': page > 1,
        'has_next': page * per_page < total,
    }