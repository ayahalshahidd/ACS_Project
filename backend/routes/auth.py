from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from database import get_db
from models.user import User

router = APIRouter()

# --- SECURITY CONFIGURATION ---
SECRET_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_STRING_IN_PROD"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing Config (Bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- HELPER FUNCTIONS ---

def verify_password(plain_password, hashed_password):
    """Checks plain password against Bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Generates Bcrypt hash."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates a signed JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- ROUTES ---

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(
    response: Response,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Secure Login: Uses Bcrypt for password check and issues HttpOnly JWT Cookie.
    """
    user = db.query(User).filter(User.email == login_data.email).first()
    
    # FIX: Changed 'user.password' to 'user.password_hash' to match your Model
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create Session Token (JWT)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "role": user.role.value}, # .value handles Enum serialization
        expires_delta=access_token_expires
    )

    # Set Secure Cookie
    response.set_cookie(
        key="session_token",
        value=access_token,
        httponly=True,
        max_age=1800,
        samesite='lax', 
        secure=False 
    )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }

@router.post("/logout")
async def logout(response: Response):
    """Clear the session cookie"""
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}

@router.post("/reset-password-dev")
async def reset_password_dev(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    DEV ONLY: Hashes the provided password with Bcrypt and saves it.
    """
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # FIX: Changed 'user.password' to 'user.password_hash' here too
    user.password_hash = get_password_hash(request.password)
    db.commit()
    return {"message": f"Password for {user.email} updated to Bcrypt hash"}