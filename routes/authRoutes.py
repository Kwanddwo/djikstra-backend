from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from db.db import get_db
from schemas import schemas
from helpers import authHelpers
from services import authService

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return authService.register_user(user, db)


@router.post("/login", response_model=schemas.Token)
def login(
    response: Response ,
    form_data: schemas.UserLogin,
    db: Session = Depends(get_db),

):
    token_data = authService.login_user(form_data, db)

    response.set_cookie(
        key="access_token",
        value=token_data["access_token"],
        httponly=True,     
        secure=False,     
        samesite="lax"     
    )

    return token_data