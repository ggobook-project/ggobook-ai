import os
import re
from google import genai
from dotenv import load_dotenv
from models.novel_format_model import NovelFormatResponse
from utils.prompt_util import PromptUtil

load_dotenv(override=True)

try:
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
except Exception as e:
    print(f"경고: 구글 API 클라이언트 초기화 실패 ({e})")
    client = None


def _regex_format_dialogue(text: str) -> str:
    """AI 실패 시 정규식 기반 대사 감지 폴백.
    한국어 서술문은 대부분 '~다.'로 끝나므로 그 외는 대사로 판단.
    """
    narrative_pattern = re.compile(r'다[.!?]$')
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    result = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if narrative_pattern.search(s):
            result.append(s)
        elif re.search(r'[.!?]$', s):
            result.append(f'"{s}"')
        else:
            result.append(s)
    return ' '.join(result)


def format_novel_dialogue(text: str) -> NovelFormatResponse:
    prompt = PromptUtil.get_format_dialogue_prompt(text)

    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            return NovelFormatResponse(formatted_text=response.text.strip())
        except Exception as e:
            print(f"AI 대사 포맷 오류 (폴백 사용): {e}")

    formatted = _regex_format_dialogue(text)
    return NovelFormatResponse(formatted_text=formatted)
