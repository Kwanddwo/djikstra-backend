from fastapi import APIRouter
from schemas.schemas import ChatRequest
from services import aiService

router = APIRouter()

@router.post("/ai-chat")
async def ai_chat(req: ChatRequest):
    return aiService.get_response(req)