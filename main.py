# app/main.py
import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

INFERENCE_URL     = os.getenv("INFERENCE_URL")
INFERENCE_KEY     = os.getenv("INFERENCE_KEY")
INFERENCE_MODEL_ID = os.getenv("INFERENCE_MODEL_ID")

class ChatRequest(BaseModel):
    user_input: str

@app.post("/ai-chat")
async def ai_chat(req: ChatRequest):
    if not all([INFERENCE_URL, INFERENCE_KEY, INFERENCE_MODEL_ID]):
        raise HTTPException(500, "AI service not configured")
    payload = {
        "model": INFERENCE_MODEL_ID,
        "messages": [
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
