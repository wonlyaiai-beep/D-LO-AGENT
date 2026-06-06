from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
from dlo_agent import get_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.post("/chat/completions")
async def chat(request: ChatRequest):
    session_id = str(uuid.uuid4())
    user_message = request.messages[-1].content
    response = await get_response(session_id, user_message)
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "model": "gpt-3.5-turbo",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response
            },
            "finish_reason": "stop"
        }]
    }

@app.get("/health")
async def health():
    return {"status": "D'LO Voice Agent Online!"}