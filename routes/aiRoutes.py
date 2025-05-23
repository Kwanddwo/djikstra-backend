from fastapi import APIRouter, Depends, Request
from schemas.schemas import ChatRequest
from services import aiService
from helpers.authHelpers import get_current_user
from models.models import User
from db.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/ai-chat")
async def ai_chat(
    req: ChatRequest, 
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda r, d=Depends(get_db): get_current_user(r, d))
):
    return aiService.get_response(req, db, current_user)