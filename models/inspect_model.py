from pydantic import BaseModel


# 검수 요청을 위한 데이터 모델
class InspectRequest(BaseModel):
    text: str  # 스프링에서 "text"라는 키로 보내는 원고 내용


# 검수 결과를 돌려줄 데이터 모델
class InspectResponse(BaseModel):
    result: str
