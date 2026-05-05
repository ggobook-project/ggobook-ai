import os
import httpx
from google import genai
from dotenv import load_dotenv
from models.chatbot_model import ChatMessage, ChatResponse
from typing import Optional

# .env 파일에서 환경변수 불어옴
load_dotenv()

SYSTEM_PROMPT = """당신은 꼬북(GGoBook) 웹툰·웹소설 플랫폼의 친절한 AI 도우미 '꼬북이'입니다.

[플랫폼 안내]
- 포인트 충전: 마이페이지 > 포인트 탭에서 충전 가능합니다.
- 작품 구매: 유료 회차 클릭 시 포인트로 구매 가능합니다. (회차당 200P)
- 회원가입: 상단 메뉴에서 회원가입 버튼을 클릭하세요.
- 환불 정책: 구매 후 열람하지 않은 회차에 한해 환불 가능합니다.
- 작품 등록: 작가 신청 후 마이페이지에서 작품 등록이 가능합니다.
- 릴레이 소설: 여러 작가가 함께 이어쓰는 소설 기능입니다.
- TTS 기능: 웹소설 뷰어에서 AI 음성으로 소설을 들을 수 있습니다.

작품 추천 요청이 오면 반드시 아래 제공된 작품 목록에서만 추천해주세요.
목록에 없는 작품은 절대 추천하지 마세요.
모르는 내용은 솔직하게 모른다고 하고, 항상 한국어로 답변하세요.
답변은 간결하게 3~5문장 이내로 해주세요."""

RECOMMEND_KEYWORDS = ["추천", "작품 추천", "웹툰 추천", "웹소설 추천", "재밌는", "볼만한"]

# Gemini 클라이언트 초기화
try:
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
except Exception as e:
    print(f"AI 클라이언트 초기화 실패 : ({e})")
    client = None

def get_contents():
    try:
        response = httpx.get("http://localhost:8080/api/contents/?size=20")
        data = response.json()
        contents = data.get("content", [])
        contents_text = "\n".join([
            f"- {c['title']} ({c['type']}, {c['genre']}): {c.get('summary', '')}"
            for c in contents
        ])
        return contents_text
    except Exception as e:
        print(f"작품 목록 가져오기 실패: {e}")
        return None

def get_read_contents(token: str):
    try:
        response = httpx.get(f"http://localhost:8080/api/readings/contents",
                             headers={"Authorization": f"Bearer {token}"})
        data = response.json()
        if not data:
            return None
        read_text = "\n".join([
            f"- {c['title']} ({c['type']}, {c['genre']})"
            for c in data
        ])
        return read_text
    except Exception as e:
        print(f"읽은 작품 가져오기 실패: {e}")
        return None

def is_recommend_question(text: str) -> bool:
    result = any(keyword in text for keyword in RECOMMEND_KEYWORDS)
    return result

def chat(messages: list[ChatMessage], user_id: Optional[int] = None, token: Optional[str] = None) -> ChatResponse:
    print(f"userId: {user_id}")
    if not client:
        return ChatResponse(reply="죄송합니다. 현재 꼬북이 AI 서비스를 이용할 수 없습니다.")

    try:
        # 대화 기록 -> 텍스트 변환
        # 마지막 대화 제외한 메세지 기록
        history = "\n".join([
            f"{'사용자' if m.role == 'user' else '꼬북이'} : {m.content}"
            for m in messages[:-1]
        ])
        # 마지막 메세지
        last_message = messages[-1].content

        contents_prompt = ""
        if is_recommend_question(last_message):
            contents_text = get_contents()
            if contents_text:
                if token:
                    read_text = get_read_contents(token)
                    print(f"읽은 작품: {read_text}")
                    if read_text:
                        contents_prompt = f"""

                        현재 플랫폼 작품 목록:
                        {contents_text}

                        이 사용자가 읽은 작품:
                        {read_text}

                        읽은 작품의 장르와 취향을 분석해서 비슷한 작품을 추천해주세요.
                        반드시 작품 목록에 있는 작품만 추천하세요."""
                    else:
                        contents_prompt = f"\n\n현재 플랫폼 작품 목록:\n{contents_text}\n\n반드시 위 목록에 있는 작품만 추천해주세요."
                else:
                    contents_prompt = f"\n\n현재 플랫폼 작품 목록:\n{contents_text}\n\n반드시 위 목록에 있는 작품만 추천해주세요."

        prompt = f"{SYSTEM_PROMPT}{contents_prompt}\n\n{history}\n사용자: {last_message}\n꼬북이:"

        # Gemini API 호출
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt
        )
        return ChatResponse(reply=response.text.strip())
    except Exception as e:
        print(f"꼬북이 AI 오류: {e}")
        return ChatResponse(reply = "죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")