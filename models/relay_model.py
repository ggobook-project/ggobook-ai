from pydantic import BaseModel


# 1. 스프링 부트가 파이썬으로 보내는 요청(Request) 데이터 상자
class RelaySummarizeRequest(BaseModel):
    entry_text: str  # 검열하고 요약할 원문 데이터


# 2. 파이썬이 스프링 부트로 돌려주는 응답(Response) 데이터 상자
class RelaySummarizeResponse(BaseModel):
    safe_summary: str  # 부적절한 내용을 제거한 건전한 요약본
