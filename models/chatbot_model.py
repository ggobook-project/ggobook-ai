# pydantic : 데이터 유효성 검사 라이브러리
# pydantic 없이 그냥 메세지 자체를 보내면 검증이 불가능
from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    # str 이라고 지정을 해주면 반드시 문자열이어야 한다고 검증함.
    # 잘못된 데이터가 들어오면 에러 발생됨.
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    userId: Optional[int] = None
    token: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str

