from utils.prompt_util import PromptUtil


class InspectService:
    def __init__(self):
        self.prompt_util = PromptUtil()

    async def summarize_content(self, text: str) -> str:
        prompt = self.prompt_util.get_summary_prompt(text)
        # TODO: 실제 LLM API 호출 (예: Anthropic Claude 또는 OpenAI)
        # response = await call_llm(prompt)
        return f"[AI 요약본] {text[:20]}... 에 대한 요약 결과입니다."

    async def moderate_content(self, text: str) -> str:
        prompt = self.prompt_util.get_moderate_prompt(text)
        # AI에게 부적절성 판단 요청
        return "PASS"  # 또는 "REJECT: 사유"

    async def moderate_relay_entry(self, text: str) -> str:
        # 릴레이 소설의 이어쓰기 내용이 적절한지 검사
        return "릴레이 소설 참여가 승인되었습니다."
