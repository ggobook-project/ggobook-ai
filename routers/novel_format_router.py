from fastapi import APIRouter
from models.novel_format_model import NovelFormatRequest, NovelFormatResponse
from services.novel_format_service import format_novel_dialogue

router = APIRouter(prefix="/api/novel", tags=["Novel Format"])


@router.post("/format-dialogue", response_model=NovelFormatResponse)
async def format_dialogue(request: NovelFormatRequest):
    """
    [POST] /api/novel/format-dialogue
    소설 원고에서 대사를 자동 감지하여 큰따옴표("")로 감싸 반환합니다.
    멀티보이스 TTS 포맷 준비용 엔드포인트입니다.
    """
    return format_novel_dialogue(request.text)
