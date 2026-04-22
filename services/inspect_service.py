import os
from google import genai
from dotenv import load_dotenv
from utils.prompt_util import PromptUtil

load_dotenv()


class InspectService:
    def __init__(self):
        self.prompt_util = PromptUtil()
        try:
            # 🌟 Client 초기화
            self.client = genai.Client()
        except Exception as e:
            print(f"🚨 경고: 구글 API 클라이언트 초기화 실패 ({e})")

    async def summarize_content(self, text: str) -> str:
        """작품 줄거리 요약 (스포일러 방지)"""
        prompt = self.prompt_util.get_summary_prompt(text)
        try:
            response = await self.client.aio.models.generate_content(
                model="gemini-3.1-flash-lite-preview", contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"🚨 줄거리 요약 AI 에러: {e}")
            return "시스템 오류로 요약본을 생성하지 못했습니다."

    async def moderate_content(self, text: str) -> str:
        """신규 작품 자동 검수 (PASS or REJECT)"""
        prompt = self.prompt_util.get_moderate_prompt(text)
        try:
            response = await self.client.aio.models.generate_content(
                model="gemini-3.1-flash-lite-preview", contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"🚨 작품 검수 AI 에러: {e}")
            return "REJECT: AI 통신 장애로 인한 자동 보류 (관리자 확인 필요)"

    async def moderate_relay_entry(self, text: str) -> str:
        """릴레이 소설 이어쓰기 자동 검수"""
        # 🌟 하드코딩 삭제 -> PromptUtil 사용!
        prompt = self.prompt_util.get_relay_moderate_prompt(text)
        try:
            response = await self.client.aio.models.generate_content(
                model="gemini-3.1-flash-lite-preview", contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"🚨 릴레이 검수 AI 에러: {e}")
            return "REJECT: 시스템 검수 실패 (관리자 확인 필요)"
