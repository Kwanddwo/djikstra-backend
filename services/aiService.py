import os
import httpx
from fastapi import HTTPException
from profanity_check import predict
from schemas.schemas import ChatRequest
from models.models import User, PromptLog
from datetime import datetime, timedelta, timezone
from helpers.skillHelpers import get_user_learning_levels

DAILY_LIMIT = 10_000
INFERENCE_URL     = os.getenv("INFERENCE_URL")
INFERENCE_KEY     = os.getenv("INFERENCE_KEY")
INFERENCE_MODEL_ID = os.getenv("INFERENCE_MODEL_ID")

SYSTEM_PROMPT_BASE = (
    "You are an intelligent AI tutor called Vertex0 on a platform called DijkstraVerse that helps users learn graph algorithms. "
    "Provide step-by-step explanations, avoid giving direct answers, and tailor your help "
    "to the user's current skill level."
)

async def get_response(req: ChatRequest, db, user: User):
    if not quota_ok(user, db):
        raise HTTPException(429, "Daily token limit reached.")
    
    if not all([INFERENCE_URL, INFERENCE_KEY, INFERENCE_MODEL_ID]):
        raise HTTPException(500, "AI service not configured")
    
    if predict([req.user_input])[0] == 1:
        return {"reply": "Hey, I'd love to help you, but I can't assist with that kind of content. Please ask me something else."}

    user_ctx = get_user_learning_levels(str(user.id), db)
    
    system_prompt = (
        f"{SYSTEM_PROMPT_BASE} "
        f"Here is the user's current Learning levels, they range from 0 to 1, 0 is Beginner, 1 is master, if it's empty then the user hasn't started a course: {user_ctx['Learning Levels']}."
        + (f" Additional context: {req.additional_context}" if req.additional_context is not None else "")
    )
    # Start with system message
    messages = [{"role": "system", "content": system_prompt}]
    
    last_log = None
    if req.additional_context is not None and "multiple_choice question incorrectly. Here are the details" in req.additional_context:    
        # Get the last message exchange for this user
        last_log = db.query(PromptLog).filter(
            PromptLog.user_id == user.id
        ).order_by(PromptLog.timestamp.desc()).first()
        
    # Include last exchange if it exists
    if last_log:
            messages.append({"role": "user", "content": last_log.user_prompt})
            messages.append({"role": "assistant", "content": last_log.llm_response})
        
    # Add current user message
    messages.append({"role": "user", "content": req.user_input})

    payload = {
        "model": INFERENCE_MODEL_ID,
        "messages": messages,
        "max_tokens": 1000,
    }

    headers = {
        "Authorization": f"Bearer {INFERENCE_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{INFERENCE_URL}/v1/chat/completions", json=payload, headers=headers, timeout=30)
        except httpx.ReadTimeout:
            raise HTTPException(504, "AI service took too long (More than 30 seconds) please simplify your request or try again later.")
        except httpx.RequestError as e:
            raise HTTPException(500, f"AI service request error: {e}")

    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"AI error: {resp.text}")
    
    data = resp.json()
    total_tokens = data["usage"]["total_tokens"]
    update_user_tokens_used(user, total_tokens, db)
    
    # Log the prompt
    prompt_log = PromptLog(
        user_id=user.id,
        user_prompt=req.user_input,  # Store just the user input
        llm_response=data["choices"][0]["message"]["content"],
        tokens_used=total_tokens,
    )
    db.add(prompt_log)
    db.commit()
    return {"reply": data["choices"][0]["message"]["content"]}


def update_user_tokens_used(user: User, tokens: int, db):
    user.tokens_used += tokens
    db.commit()

def quota_ok(user: User, db):
    # Ensure last_reset is timezone-aware
    last_reset = user.last_reset
    if last_reset.tzinfo is None:
        last_reset = last_reset.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) - last_reset > timedelta(days=1):
        user.tokens_used = 0
        user.last_reset = datetime.now(timezone.utc)
        db.commit()
    if user.tokens_used >= DAILY_LIMIT:
        raise HTTPException(429, "Daily token limit reached.")
    return user
