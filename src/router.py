# llm.py
# LLM Inference Routes
from uuid import uuid4

from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse

# import llm chat_complete function
from .llm import chat_complete
# import models
from .models import ChatMessage, ChatResponse

# create a simple router
router = APIRouter(
    prefix="/api/v1",
    tags=["llm", "ai", ],
)


@router.post("/chat", response_model=None)
async def chat(message: ChatMessage, session_id: str = None) -> JSONResponse | StreamingResponse:
    """Chat Completion Endpoint"""
    try:
        if session_id is None:
            session_id = str(uuid4())
        return await chat_complete(message, session_id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
