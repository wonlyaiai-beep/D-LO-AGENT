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
        chunk = {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "model": "custom",
            "choices": [{
                "index": 0,
                "delta": {
                    "role": "assistant",
                    "content": response
                },
                "finish_reason": None
            }]
        }
        yield f"data: {json.dumps(chunk)}\n\n"

        final = {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "model": "custom",
            "choices": [{
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }]
        }
        yield f"data: {json.dumps(final)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )

@app.get("/health")
async def health():
    return {"status": "D'LO Voice Agent Online!"}