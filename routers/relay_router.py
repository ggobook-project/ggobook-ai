from fastapi import APIRouter
from models.relay_model import RelaySummarizeRequest, RelaySummarizeResponse
from services.relay_service import summarize_relay_entry

# 라우터 객체 생성 (주소 묶음)
router = APIRouter(prefix="/api/relay", tags=["Relay Novel"])


@router.post("/summarize", response_model=RelaySummarizeResponse)
async def summarize_entry(request: RelaySummarizeRequest):
    """
    [POST] /api/relay/summarize
    스프링 부트로부터 원문을 받아 AI 요약본을 반환하는 엔드포인트입니다.
    """
    # 서비스 로직을 호출하여 요약 결과를 받아옵니다.
    result = summarize_relay_entry(request.entry_text)
    return result
