from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import uuid
import json
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
    
    async def generate():