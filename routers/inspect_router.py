from fastapi import APIRouter
from models.inspect_model import InspectRequest
from services.inspect_service import InspectService
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/inspect", tags=["inspect"])
inspect_service = InspectService()


@router.post("/summary")
async def summarize_content(request: InspectRequest):
    result = await inspect_service.summarize_content(request.text)
    # 스프링 부트의 RestTemplate이 String을 원하므로 PlainTextResponse 사용
    return PlainTextResponse(content=result)


@router.post("/moderate")
async def moderate_content(request: InspectRequest):
    result = await inspect_service.moderate_content(request.text)
    return PlainTextResponse(content=result)


@router.post("/relay")
async def moderate_relay_entry(request: InspectRequest):
    result = await inspect_service.moderate_relay_entry(request.text)
    return PlainTextResponse(content=result)
