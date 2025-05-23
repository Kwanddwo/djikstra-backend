from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from models.models import User
from db.db import get_db

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 30)

if not SECRET_KEY or not ALGORITHM:
    raise RuntimeError("Missing SECRET_KEY or ALGORITHM environment variables")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            return None
        return id
    except ExpiredSignatureError:
        print("Token has expired")
        return None
    except InvalidTokenError:
        return None
    
# New function to extract token from request
def extract_token_from_request(request: Request):
    # Try to get from cookies first
    token = request.cookies.get("access_token")
    
    # If not in cookies, try Authorization header
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
    
    return token
    
def get_current_user(request: Request = Depends(), db: Session = Depends(get_db)):
    token = extract_token_from_request(request)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user