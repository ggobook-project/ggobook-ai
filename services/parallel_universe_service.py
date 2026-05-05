import os
from google import genai
from dotenv import load_dotenv
from models.parallel_universe_model import ParallelUniverseRequest, ParallelUniverseResponse

load_dotenv()

try:
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
except Exception as e:
    print(f"AI 클라이언트 초기화 실패: ({e})")
    client = None


def generate_parallel_universe(request: ParallelUniverseRequest) -> ParallelUniverseResponse:
    if not client:
        return ParallelUniverseResponse(parallel_universe_text="죄송합니다. 현재 AI 서비스를 이용할 수 없습니다.")

    try:
        prompt = f"""당신은 창의적인 웹소설 작가입니다.
아래 작품의 세계관과 등장인물 성격을 그대로 유지한 채 짧은 평행우주 외전을 작성해주세요.

[작품 제목]
{request.title}

[작품 줄거리]
{request.summary}

[현재 회차 내용]
{request.content_text}

[만약에...?]
{request.what_if}

위 조건으로 500자 내외의 짧은 외전을 작성해주세요.
등장인물의 말투와 성격을 원작과 동일하게 유지하세요.
한국어로 작성해주세요."""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return ParallelUniverseResponse(parallel_universe_text=response.text.strip())

    except Exception as e:
        print(f"평행우주 생성 오류: {e}")
        return ParallelUniverseResponse(parallel_universe_text="죄송합니다. 외전 생성 중 오류가 발생했습니다.")