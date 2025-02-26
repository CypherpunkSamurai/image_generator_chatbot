from typing import List, Optional

from pydantic import BaseModel


class ChatMessage(BaseModel):
    session_id: Optional[str] = None
    message: str
    model: str = "gpt-4-0314"
    stream: bool = False


class ChatResponse(BaseModel):
    session_id: str
    response: str
    history: List[dict]
    # added later
    model: str
