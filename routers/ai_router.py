from fastapi import APIRouter
from pydantic import BaseModel

# '/api/ai' 주소로 들어오는 요청을 담당하는 라우터 생성
router = APIRouter(prefix="/api/ai", tags=["AI API"])


# 프론트엔드/백엔드에서 우리에게 보낼 데이터의 뼈대(규칙)
class AIRequest(BaseModel):
    prompt: str


# POST 방식으로 데이터를 받아오는 창구 만들기
@router.post("/generate")
def generate_ai_text(request: AIRequest):
    # 나중에 이 부분에 진짜 LLM(ChatGPT 등) 모델을 연결할 겁니다!
    return {
        "status": "success",
        "received_message": request.prompt,
        "ai_response": "GGoBook AI 통신이 완벽하게 연결되었습니다! 꼬북!",
    }
