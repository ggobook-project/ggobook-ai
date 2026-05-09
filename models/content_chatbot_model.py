from pydantic import BaseModel
from typing import List, Optional


class ContentChatMessage(BaseModel):
    role: str
    content: str


class ContentChatRequest(BaseModel):
    messages: List[ContentChatMessage]
    contentId: int
    currentEpisodeId: int
    token: Optional[str] = None


class ContentChatResponse(BaseModel):
    reply: str
