"""
Security utilities for authentication, authorization, and token management.
Handles JWT tokens, password hashing, and security validation.
"""

import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
import structlog

from app.core.config import settings
from app.models.schemas import TokenPayload

logger = structlog.get_logger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer token scheme
security = HTTPBearer()


class SecurityManager:
    """Centralized security management for the application."""
    
    def __init__(self):
        self.algorithm = settings.ALGORITHM
        self.secret_key = settings.SECRET_KEY
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES
    
    def create_access_token(
        self, 
        subject: Union[str, Any], 
        expires_delta: Optional[timedelta] = None,
        additional_claims: Optional[Dict] = None
    ) -> str:
        """Create JWT access token."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": "access",
            "iat": datetime.utcnow(),
        }
        
        if additional_claims:
            to_encode.update(additional_claims)
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        
        logger.info("Access token created", subject=subject, expires=expire)
        return encoded_jwt
    
    def create_refresh_token(
        self, 
        subject: Union[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT refresh token."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.refresh_token_expire_minutes)
        
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": "refresh",
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(32),  # Unique token ID
        }
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        
        logger.info("Refresh token created", subject=subject, expires=expire)
        return encoded_jwt
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[TokenPayload]:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Validate token type
            if payload.get("type") != token_type:
                logger.warning("Invalid token type", expected=token_type, actual=payload.get("type"))
                return None
            
            # Check expiration
            exp = payload.get("exp")
            if exp is None or datetime.fromtimestamp(exp) < datetime.utcnow():
                logger.warning("Token expired", exp=exp)
                return None
            
            # Extract subject
            subject = payload.get("sub")
            if subject is None:
                logger.warning("Token missing subject")
                return None
            
            return TokenPayload(sub=subject, exp=exp, **payload)
            
        except JWTError as e:
            logger.warning("JWT verification failed", error=str(e))
            return None
        except ValidationError as e:
            logger.warning("Token payload validation failed", error=str(e))
            return None
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def generate_password_reset_token(self, email: str) -> str:
        """Generate password reset token."""
        delta = timedelta(hours=1)  # Reset token expires in 1 hour
        now = datetime.utcnow()
        expires = now + delta
        
        to_encode = {
            "exp": expires,
            "sub": email,
            "type": "password_reset",
            "iat": now,
        }
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_password_reset_token(self, token: str) -> Optional[str]:
        """Verify password reset token and return email."""
        payload = self.verify_token(token, token_type="password_reset")
        if payload:
            return payload.sub
        return None
    
    def generate_email_verification_token(self, email: str) -> str:
        """Generate email verification token."""
        delta = timedelta(hours=24)  # Verification token expires in 24 hours
        now = datetime.utcnow()
        expires = now + delta
        
        to_encode = {
            "exp": expires,
            "sub": email,
            "type": "email_verification",
            "iat": now,
        }
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_email_verification_token(self, token: str) -> Optional[str]:
        """Verify email verification token and return email."""
        payload = self.verify_token(token, token_type="email_verification")
        if payload:
            return payload.sub
        return None


# Global security manager instance
security_manager = SecurityManager()


def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create access token - convenience function."""
    return security_manager.create_access_token(subject, expires_delta)


def create_refresh_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create refresh token - convenience function."""
    return security_manager.create_refresh_token(subject, expires_delta)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password - convenience function."""
    return security_manager.verify_password(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password - convenience function."""
    return security_manager.hash_password(password)


def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength and return detailed feedback."""
    issues = []
    score = 0
    
    # Length check
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        issues.append(f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long")
    else:
        score += 1
    
    # Character variety checks
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    if not has_lower:
        issues.append("Password must contain at least one lowercase letter")
    else:
        score += 1
    
    if not has_upper:
        issues.append("Password must contain at least one uppercase letter")
    else:
        score += 1
    
    if not has_digit:
        issues.append("Password must contain at least one digit")
    else:
        score += 1
    
    if not has_special:
        issues.append("Password must contain at least one special character")
    else:
        score += 1
    
    # Common password checks
    common_passwords = [
        "password", "123456", "password123", "admin", "qwerty",
        "letmein", "welcome", "monkey", "1234567890"
    ]
    
    if password.lower() in common_passwords:
        issues.append("Password is too common")
        score = max(0, score - 2)
    
    # Calculate strength
    if score >= 5:
        strength = "strong"
    elif score >= 3:
        strength = "medium"
    else:
        strength = "weak"
    
    return {
        "valid": len(issues) == 0,
        "strength": strength,
        "score": score,
        "issues": issues,
    }


class RateLimiter:
    """Rate limiting for authentication endpoints."""
    
    def __init__(self):
        self.attempts = {}  # In production, use Redis
    
    def is_rate_limited(self, identifier: str, limit: int = 5, window: int = 300) -> bool:
        """Check if identifier is rate limited."""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window)
        
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        
        # Clean old attempts
        self.attempts[identifier] = [
            attempt for attempt in self.attempts[identifier]
            if attempt > window_start
        ]
        
        return len(self.attempts[identifier]) >= limit
    
    def record_attempt(self, identifier: str) -> None:
        """Record an authentication attempt."""
        now = datetime.utcnow()
        
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        
        self.attempts[identifier].append(now)
    
    def clear_attempts(self, identifier: str) -> None:
        """Clear recorded attempts for identifier."""
        if identifier in self.attempts:
            del self.attempts[identifier]


# Global rate limiter instance
rate_limiter = RateLimiter()


def generate_api_key() -> str:
    """Generate secure API key."""
    return secrets.token_urlsafe(32)


def validate_api_key(api_key: str) -> bool:
    """Validate API key format."""
    # Basic validation - in production, check against database
    return len(api_key) >= 32 and api_key.replace("-", "").replace("_", "").isalnum()


class SecurityHeaders:
    """Security headers for HTTP responses."""
    
    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """Get recommended security headers."""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }


def create_session_token() -> str:
    """Create secure session token."""
    return secrets.token_urlsafe(64)


def constant_time_compare(a: str, b: str) -> bool:
    """Constant-time string comparison to prevent timing attacks."""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    
    return result == 0