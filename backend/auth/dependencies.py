from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# --- FIX: Import get_db correctly ---
# If this file is in backend/auth/dependencies.py, we import from the root 'database'
from database import get_db
from models.user import User

# CONFIGURATION
# IMPORTANT: This SECRET_KEY must be identical to the one in your login route!
SECRET_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_STRING_IN_PROD"  
ALGORITHM = "HS256"

# This tells FastAPI that the token comes from the "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)  # Now get_db is defined and will work
):
    """
    Decodes the JWT token, extracts the email, and retrieves the user from the DB.
    If anything is wrong (expired token, invalid signature, user deleted), it throws 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decode the Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 2. Extract the Subject (usually email or ID)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # 3. Check if User exists in Database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user