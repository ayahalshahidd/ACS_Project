"""
Debug/Info routes
VULNERABLE: Exposes sensitive system information
This should NEVER be enabled in production
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, engine
from models.user import User
import os
import sys

router = APIRouter()


@router.get("/info")
async def get_system_info():
    """
    Get system information
    VULNERABLE: Exposes sensitive system and configuration information
    This endpoint should be disabled in production
    """
    # VULNERABLE: Exposing environment variables (may contain secrets)
    env_vars = {k: v for k, v in os.environ.items() if 'PASSWORD' in k.upper() or 'SECRET' in k.upper() or 'KEY' in k.upper()}
    
    # VULNERABLE: Exposing database connection string
    db_url = str(engine.url) if hasattr(engine, 'url') else "Unknown"
    
    return {
        "system_info": {
            "python_version": sys.version,
            "platform": sys.platform,
            "executable": sys.executable,
        },
        "database": {
            "connection_string": db_url,  # VULNERABLE: Exposing database credentials
            "driver": engine.driver if hasattr(engine, 'driver') else "Unknown"
        },
        "environment": {
            "sensitive_vars": env_vars,  # VULNERABLE: Exposing environment variables with secrets
            "all_env_vars": dict(os.environ)  # VULNERABLE: Exposing ALL environment variables
        },
        "application": {
            "working_directory": os.getcwd(),
            "file_paths": {
                "database_file": "database.db" if os.path.exists("database.db") else None,
                "cert_file": "cert.pem" if os.path.exists("cert.pem") else None,
                "key_file": "key.pem" if os.path.exists("key.pem") else None
            }
        }
    }


@router.get("/users/export")
async def export_all_users(
    db: Session = Depends(get_db)
):
    """
    Export all user data
    VULNERABLE: Exposes all sensitive user data including password hashes
    This should require admin authentication and proper authorization
    """
    users = db.query(User).all()
    
    # VULNERABLE: Returning ALL sensitive user data in plaintext
    return {
        "total_users": len(users),
        "users": [
            {
                "id": user.id,
                "email": user.email,
                "password_hash": user.password_hash,  # VULNERABLE: Exposing password hash
                "role": user.role.value,
                "student_id": user.student_id,  # VULNERABLE: Exposing PII
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            for user in users
        ],
        "warning": "This endpoint exposes sensitive data and should be protected"
    }

