from fastapi import APIRouter, Depends, Response, Request
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
        secure=True,     
        samesite="lax"     
    )

    return token_data

@router.post("/verify", response_model=schemas.UserOut)
def verify(
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
):
    token = authHelpers.extract_token_from_request(request)
    if not token:
        response.status_code = 401
        return {"detail": "Token not found"}
    user = authHelpers.verify_token(token, db)
    if not user:
        response.status_code = 401
        return {"detail": "Invalid token"}
    return {"detail": "Token is valid", "user": user}