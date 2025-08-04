"""
Main FastAPI application for CDST Diagnostic Network Optimization Platform.
Handles application startup, middleware configuration, and route registration.
"""

import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware
import structlog
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from app.core.config import settings
from app.core.database import init_db, close_db, check_db_health
from app.core.cache import init_redis, close_redis
from app.core.logging import setup_logging
from app.api.v1.api import api_router
from app.middleware.rate_limiting import RateLimitMiddleware
from app.middleware.authentication import AuthenticationMiddleware
from app.middleware.audit import AuditMiddleware

# Setup structured logging
setup_logging()
logger = structlog.get_logger(__name__)

# Initialize Sentry for error tracking
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[
            FastApiIntegration(auto_enabling=True),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=0.1,
        environment="production" if not settings.DEBUG else "development",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    logger.info("Starting CDST Optimization Platform")
    
    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized")
        
        # Initialize Redis cache
        await init_redis()
        logger.info("Redis cache initialized")
        
        # Check external services
        if settings.ENABLE_ROUTING_API:
            # Test OSRM routing service
            from app.services.routing import test_routing_service
            if await test_routing_service():
                logger.info("Routing service is available")
            else:
                logger.warning("Routing service is not available, using fallback")
        
        logger.info("Application startup completed successfully")
        
    except Exception as e:
        logger.error("Failed to start application", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down CDST Optimization Platform")
    
    try:
        await close_db()
        await close_redis()
        logger.info("Application shutdown completed")
    except Exception as e:
        logger.error("Error during application shutdown", error=str(e))


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Add middleware in reverse order (last added = first executed)

# CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.DEBUG else ["localhost", "127.0.0.1"]
)

# Session middleware for session management
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    same_site="lax",
    https_only=not settings.DEBUG,
)

# Custom middleware
app.add_middleware(AuditMiddleware)
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(RateLimitMiddleware)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with structured logging."""
    logger.warning(
        "HTTP exception occurred",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
        method=request.method,
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "http_error"
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.warning(
        "Validation error occurred",
        errors=exc.errors(),
        path=request.url.path,
        method=request.method,
    )
    
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": 422,
                "message": "Validation failed",
                "type": "validation_error",
                "details": exc.errors()
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(
        "Unhandled exception occurred",
        error=str(exc),
        path=request.url.path,
        method=request.method,
        exc_info=True,
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error" if not settings.DEBUG else str(exc),
                "type": "internal_error"
            }
        }
    )


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with timing information."""
    start_time = time.time()
    
    # Log request
    logger.info(
        "Request started",
        method=request.method,
        path=request.url.path,
        query_params=str(request.query_params),
        client_ip=request.client.host if request.client else None,
    )
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(
        "Request completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        process_time=f"{process_time:.3f}s",
    )
    
    # Add timing header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.APP_VERSION,
    }


@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check():
    """Detailed health check with dependency status."""
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.APP_VERSION,
        "services": {}
    }
    
    # Check database
    try:
        db_healthy = await check_db_health()
        health_status["services"]["database"] = "healthy" if db_healthy else "unhealthy"
    except Exception as e:
        health_status["services"]["database"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check Redis cache
    try:
        from app.core.cache import check_redis_health
        redis_healthy = await check_redis_health()
        health_status["services"]["redis"] = "healthy" if redis_healthy else "unhealthy"
    except Exception as e:
        health_status["services"]["redis"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check external routing service
    if settings.ENABLE_ROUTING_API:
        try:
            from app.services.routing import test_routing_service
            routing_healthy = await test_routing_service()
            health_status["services"]["routing"] = "healthy" if routing_healthy else "unhealthy"
        except Exception as e:
            health_status["services"]["routing"] = f"error: {str(e)}"
            health_status["status"] = "degraded"
    
    return health_status


# Metrics endpoint for monitoring
@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus-compatible metrics endpoint."""
    if not settings.ENABLE_METRICS:
        raise HTTPException(status_code=404, detail="Metrics not enabled")
    
    from app.core.metrics import generate_metrics
    return await generate_metrics()


# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "CDST Diagnostic Network Optimization Platform API",
        "version": settings.APP_VERSION,
        "docs_url": "/docs" if settings.DEBUG else None,
        "api_url": settings.API_V1_STR,
        "organization": "PATH - Program for Appropriate Technology in Health",
        "description": settings.APP_DESCRIPTION,
    }


# Add custom OpenAPI schema
def custom_openapi():
    """Custom OpenAPI schema with additional information."""
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        routes=app.routes,
    )
    
    # Add custom information
    openapi_schema["info"]["contact"] = {
        "name": "PATH",
        "url": "https://www.path.org",
        "email": "info@path.org"
    }
    
    openapi_schema["info"]["license"] = {
        "name": "Proprietary",
        "url": "https://www.path.org"
    }
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
    )