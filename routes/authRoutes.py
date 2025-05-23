from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas import schemas
from app.helpers import authHelpers
from app.services import authService

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return authService.register_user(user, db)


@router.post("/login", response_model=schemas.Token)
def login(
    response: Response ,
    form_data: OAuth2PasswordRequestForm = Depends(),
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