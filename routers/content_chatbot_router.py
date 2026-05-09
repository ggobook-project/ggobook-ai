from fastapi import APIRouter
from models.content_chatbot_model import ContentChatRequest, ContentChatResponse
from services.content_chatbot_service import content_chat

router = APIRouter()


@router.post("/content-chatbot/chat", response_model=ContentChatResponse)
async def content_chatbot(request: ContentChatRequest):
    return content_chat(
        request.messages,
        request.contentId,
        request.currentEpisodeId,
        request.token
    )
