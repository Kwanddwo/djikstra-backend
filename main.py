# app/main.py
import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from profanity_check import predict

app = FastAPI()

INFERENCE_URL     = os.getenv("INFERENCE_URL")
INFERENCE_KEY     = os.getenv("INFERENCE_KEY")
INFERENCE_MODEL_ID = os.getenv("INFERENCE_MODEL_ID")

# This system prompt should hold the context of the user, their skill level
# progress and what page they are on
SYSTEM_PROMPT_BASE = (
    "You are an intelligent AI tutor called Djelal that helps users learn graph algorithms. "
    "Provide step-by-step explanations, avoid giving direct answers, and tailor your help "
    "to the user's current skill level."
)

def get_user_context(user_id: str):
    # Placeholder function to get user context
    # In a real application, this would query a database or other data source
    return {
        "Learning Levels": {
            "Graph traversal": 0.85,
            "Graph basics": 0.75,
            "Graph algorithms": 0.65,
            "Graph theory": 0.55,
            "Graph data structures": 0.45,
            "Graph applications": 0.35,
            "Graph optimization": 0.25,
            "Graph complexity": 0.15,
            "Graph proofs": 0.05,
            "Graph history": 0.0,
        },
        "Current Page": "Shortest Path Algorithms"    
    }

class ChatRequest(BaseModel):
    user_input: str

@app.post("/ai-chat")
async def ai_chat(req: ChatRequest):
    if not all([INFERENCE_URL, INFERENCE_KEY, INFERENCE_MODEL_ID]):
        raise HTTPException(500, "AI service not configured")
    
    if predict([req.user_input])[0] == 1:
        return {"reply": "Hey, I'd love to help you, but I can't assist with that kind of content. Please ask me something else."}

    user_ctx = get_user_context("user_id")  # Replace with actual user ID
    
    system_prompt = (
        f"{SYSTEM_PROMPT_BASE} "
        f"Here is the user's current Learning levels, they range from 0 to 1, 0 is Beginner, 1 is master: {user_ctx["Learning Levels"]} "
        f"The user's current page is {user_ctx['Current Page']} "
    )

    payload = {
        "model": INFERENCE_MODEL_ID,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.user_input}
        ]
    }

    headers = {
        "Authorization": f"Bearer {INFERENCE_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{INFERENCE_URL}/v1/chat/completions", json=payload, headers=headers)

    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"AI error: {resp.text}")
    
    data = resp.json()
    return {"reply": data["choices"][0]["message"]["content"]}
