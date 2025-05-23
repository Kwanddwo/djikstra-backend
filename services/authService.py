from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import models
from schemas import schemas 
from helpers import authHelpers

def register_user(user: schemas.UserCreate, db: Session):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = authHelpers.get_password_hash(user.password)
    new_user = models.User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(form_data: schemas.UserLogin, db: Session):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not authHelpers.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authHelpers.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}