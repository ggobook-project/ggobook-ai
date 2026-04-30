from fastapi import APIRouter
from models.chatbot_model import ChatRequest, ChatResponse
from services.chatbot_service import chat

router = APIRouter(prefix="/api/chatbot", tags=["Chatbot"])


@router.post("/chat", response_model=ChatResponse)
async def chatbot(request: ChatRequest):
    return chat(request.messages)
