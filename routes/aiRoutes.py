from fastapi import APIRouter, Depends, Request
from schemas.schemas import ChatRequest
from services import aiService
from helpers.authHelpers import get_current_user
from models.models import User

router = APIRouter()

@router.post("/ai-chat")
async def ai_chat(req: ChatRequest, request: Request, current_user: User = Depends(get_current_user)):
    return aiService.get_response(req, current_user)