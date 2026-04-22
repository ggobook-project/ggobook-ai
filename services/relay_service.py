import os
from google import genai
from dotenv import load_dotenv
from models.relay_model import RelaySummarizeResponse
from utils.prompt_util import PromptUtil  # 🌟 유틸 임포트

# .env 파일 로드
load_dotenv()

try:
    client = genai.Client()
except Exception as e:
    print(f"🚨 경고: 구글 API 클라이언트 초기화 실패 ({e})")


def summarize_relay_entry(entry_text: str) -> RelaySummarizeResponse:
    # 🌟 하드코딩 삭제 -> PromptUtil 정적 메서드 바로 호출!
    prompt = PromptUtil.get_relay_summary_prompt(entry_text)

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", contents=prompt
        )

        summary_result = response.text.strip()
        print(f"✅ AI 요약 성공: {summary_result}")

        return RelaySummarizeResponse(safe_summary=summary_result)

    except Exception as e:
        print(f"🚨 AI Summary Error: {e}")
        return RelaySummarizeResponse(
            safe_summary="관리자에 의해 부적절한 내용이 가려진 회차입니다. (AI 응답 지연)"
        )
