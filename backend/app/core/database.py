"""
Database connection and session management.
Handles PostgreSQL with PostGIS extension for geospatial data.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from geoalchemy2 import Geography
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

# Create async engine for database operations
engine = create_async_engine(
    str(settings.DATABASE_URL),
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Create sync engine for migrations and admin tasks
sync_engine = create_engine(
    str(settings.DATABASE_URL).replace("+asyncpg", ""),
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

# Base class for all database models
Base = declarative_base()


# Database session dependency
async def get_db() -> AsyncSession:
    """
    Dependency function that yields database sessions.
    Automatically handles session cleanup and error handling.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error("Database session error", error=str(e))
            raise
        finally:
            await session.close()


# Database connection events
@event.listens_for(sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable PostGIS extension on connection."""
    if "sqlite" not in str(settings.DATABASE_URL):
        with dbapi_connection.cursor() as cursor:
            # Enable PostGIS extension
            cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis_topology;")


async def init_db() -> None:
    """Initialize database with all tables."""
    try:
        async with engine.begin() as conn:
            # Import all models to register them with Base
            from app.models import (
                user,
                laboratory,
                network,
                optimization,
                service_area,
                test_demand,
                audit,
            )
            
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database initialized successfully")
            
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise


async def close_db() -> None:
    """Close database connections."""
    try:
        await engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error("Error closing database connections", error=str(e))


# Database health check
async def check_db_health() -> bool:
    """Check if database is accessible and healthy."""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return False


# Transaction context manager
class DatabaseTransaction:
    """Context manager for database transactions."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def __aenter__(self):
        return self.session
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
            logger.error("Transaction rolled back", error=str(exc_val))
        else:
            await self.session.commit()


# Utility functions for geospatial operations
def create_point_geography(latitude: float, longitude: float) -> Geography:
    """Create a PostGIS Geography point from latitude and longitude."""
    return f"POINT({longitude} {latitude})"


def calculate_distance_query(point1: Geography, point2: Geography) -> str:
    """Generate SQL for calculating distance between two geography points."""
    return f"ST_Distance({point1}, {point2})"


# Database connection pooling for high-performance scenarios
class DatabasePool:
    """Database connection pool manager."""
    
    def __init__(self):
        self._engine = None
        self._session_factory = None
    
    async def initialize(self):
        """Initialize the connection pool."""
        self._engine = create_async_engine(
            str(settings.DATABASE_URL),
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=True,
            echo=settings.DEBUG,
        )
        
        self._session_factory = sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        logger.info("Database pool initialized")
    
    async def get_session(self) -> AsyncSession:
        """Get a database session from the pool."""
        if not self._session_factory:
            await self.initialize()
        
        return self._session_factory()
    
    async def close(self):
        """Close the connection pool."""
        if self._engine:
            await self._engine.dispose()
            logger.info("Database pool closed")


# Global database pool instance
db_pool = DatabasePool()