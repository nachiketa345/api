from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import User
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import Asy n ncSession

# Configuration

SECRET_KEY="your-secret-key-change"
ALGORITHIM="HS256"
ACCESS_TOKEN_EXPIRY=30


password_hash=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/users/login")

def get_password_hash(password: str):
    """Hash a password using bcrypt."""
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    """Verify a plain password against a hashed password."""
    return password_hash.verify(plain_password, hashed_password)


def create_token_access(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT Token"""
    to_encode=data.copy()         # Creates a shallow copy of the input dictionary
    if expires_delta:              # Check if an expiration delta is provided
        expire=datetime.utcnow() + expires_delta
    else:
        expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHIM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    """Retrieve the current user based on the provided token."""
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHIM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    
    stmt=select(User).where(User.email==email)
    result= await db.execute(stmt)
    user= result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
