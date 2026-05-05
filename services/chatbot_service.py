import os
from google import genai
from dotenv import load_dotenv
from models.chatbot_model import ChatMessage, ChatResponse

load_dotenv(override=True)

SYSTEM_PROMPT = """당신은 꼬북(GGoBook) 웹툰·웹소설 플랫폼의 친절한 AI 도우미 '꼬북이'입니다.
사용자가 플랫폼 이용 방법, 작품 등록, 회차 등록, 릴레이 소설, TTS 기능, 포인트, 마이페이지 등에 대해 질문하면 친절하고 간결하게 안내해주세요.
모르는 내용은 솔직하게 모른다고 하고, 항상 한국어로 답변하세요.
답변은 간결하게 3~5문장 이내로 해주세요."""

try:
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
except Exception as e:
    print(f"경고: 챗봇 AI 클라이언트 초기화 실패 ({e})")
    client = None


def chat(messages: list[ChatMessage]) -> ChatResponse:
    if not client:
        return ChatResponse(reply="죄송해요, 현재 AI 서비스를 사용할 수 없습니다. 잠시 후 다시 시도해주세요.")

    try:
        history = "\n".join([
            f"{'사용자' if m.role == 'user' else '꼬북이'}: {m.content}"
            for m in messages[:-1]
        ])
        last = messages[-1].content
        prompt = f"{SYSTEM_PROMPT}\n\n{history}\n사용자: {last}\n꼬북이:"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return ChatResponse(reply=response.text.strip())
    except Exception as e:
        print(f"챗봇 오류: {e}")
        return ChatResponse(reply="죄송해요, 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
