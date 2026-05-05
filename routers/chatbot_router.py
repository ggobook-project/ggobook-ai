from fastapi import APIRouter
from models.chatbot_model import ChatRequest, ChatResponse
from services.chatbot_service import chat

# Spring 의 @RestController랑 같은 역할
router = APIRouter()

# == @PostMapping
@router.post("/chatbot/chat", response_model=ChatResponse)
async def chatbot(request: ChatRequest):
    return chat(request.messages, request.userId, request.token)