import os
import httpx
from google import genai
from dotenv import load_dotenv
from models.content_chatbot_model import ContentChatMessage, ContentChatResponse
from typing import Optional, List

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")
MAX_EPISODES = 15  # 최대 가져올 에피소드 수 (너무 많으면 느림)

try:
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
except Exception as e:
    print(f"AI 클라이언트 초기화 실패: {e}")
    client = None


def _headers(token: Optional[str]) -> dict:
    return {"Authorization": f"Bearer {token}"} if token else {}


def _get_episode_list(content_id: int, token: Optional[str]) -> Optional[dict]:
    """작품 정보 + 에피소드 목록(기본 정보)을 가져온다."""
    try:
        res = httpx.get(
            f"{BACKEND_URL}/api/contents/{content_id}",
            headers=_headers(token),
            timeout=10,
        )
        if res.status_code == 401:
            print(f"contents API 401: 인증 실패")
            return None
        if res.status_code != 200:
            print(f"contents API 오류: {res.status_code}")
            return None
        return res.json()
    except Exception as e:
        print(f"contents API 호출 실패: {e}")
        return None


def _get_episode_detail(episode_id: int, token: Optional[str]) -> Optional[str]:
    """개별 에피소드 상세에서 aiSummary 또는 contentText를 가져온다."""
    try:
        res = httpx.get(
            f"{BACKEND_URL}/api/episodes/{episode_id}",
            headers=_headers(token),
            timeout=8,
        )
        if res.status_code != 200:
            print(f"[episode {episode_id}] status={res.status_code}")
            return None
        data = res.json()

        # 1) 최상위 aiSummary
        text = (data.get("aiSummary") or "").strip()
        if text:
            return text

        # 2) novel.aiSummary
        novel = data.get("novel") or {}
        text = (novel.get("aiSummary") or "").strip()
        if text:
            return text

        # 3) novel.contentText (앞 2000자)
        raw = (novel.get("contentText") or "").strip()
        if raw:
            return raw[:2000]

        # 4) 최상위 contentText
        raw = (data.get("contentText") or "").strip()
        if raw:
            return raw[:2000]

        return None
    except Exception as e:
        print(f"episode {episode_id} API 호출 실패: {e}")
        return None


def content_chat(
    messages: List[ContentChatMessage],
    content_id: int,
    current_episode_id: int,
    token: Optional[str] = None,
) -> ContentChatResponse:
    if not client:
        return ContentChatResponse(reply="AI 서비스를 현재 이용할 수 없습니다.")

    # ── 1. 작품 정보 + 에피소드 목록 ──────────────────────────────────────
    content_data = _get_episode_list(content_id, token)
    if content_data is None:
        return ContentChatResponse(
            reply="작품 정보를 불러올 수 없습니다. 로그인 상태를 확인해주세요."
        )

    title = content_data.get("title", "해당 작품")

    # episodes 필드는 페이지네이션 객체 {"content": [...]} 형태
    episodes_field = content_data.get("episodes", {})
    if isinstance(episodes_field, dict):
        episodes: list = episodes_field.get("content", [])
    elif isinstance(episodes_field, list):
        episodes = episodes_field
    else:
        episodes = []

    episodes = [e for e in episodes if isinstance(e, dict)]

    if not episodes:
        return ContentChatResponse(reply="에피소드 정보를 불러올 수 없습니다.")

    # ── 2. 현재 에피소드 번호 확인 ─────────────────────────────────────────
    current_ep = next(
        (e for e in episodes if e.get("episodeId") == current_episode_id), None
    )
    if not current_ep:
        # episodeId 타입 불일치 대비 (int vs str)
        current_ep = next(
            (e for e in episodes if str(e.get("episodeId")) == str(current_episode_id)),
            None,
        )
    if not current_ep:
        return ContentChatResponse(
            reply="현재 회차 정보를 찾을 수 없습니다. 다시 시도해주세요."
        )

    current_num: int = current_ep.get("episodeNumber", 0)

    # ── 3. 현재 회차까지의 에피소드만 필터, 정렬 ──────────────────────────
    readable = sorted(
        [e for e in episodes if e.get("episodeNumber", 0) <= current_num],
        key=lambda e: e.get("episodeNumber", 0),
    )
    # 너무 많으면 최근 MAX_EPISODES개만 사용
    if len(readable) > MAX_EPISODES:
        readable = readable[-MAX_EPISODES:]

    # ── 4. aiSummary 수집 ─────────────────────────────────────────────────
    context_parts: list[str] = []
    for ep in readable:
        ep_num = ep.get("episodeNumber", "?")
        ep_title = ep.get("episodeTitle", f"{ep_num}화")
        ep_id = ep.get("episodeId")

        # 목록 API에 이미 있는 경우 우선 사용
        summary = (ep.get("aiSummary") or "").strip()

        # 없으면 개별 에피소드 API 호출
        if not summary and ep_id:
            summary = _get_episode_detail(ep_id, token) or ""

        if summary:
            context_parts.append(f"[{ep_num}화 - {ep_title}]\n{summary}")

    if not context_parts:
        return ContentChatResponse(
            reply=(
                "회차별 요약 정보가 아직 없어서 답변이 어렵습니다. "
                "요약이 생성된 후 다시 이용해주세요."
            )
        )

    context = "\n\n".join(context_parts)

    # ── 5. 시스템 프롬프트 + LLM 호출 ────────────────────────────────────
    system_prompt = f"""당신은 '{title}' 작품의 전용 AI 챗봇입니다.

사용자는 현재 {current_num}화까지 읽었습니다.
반드시 {current_num}화까지의 내용만을 바탕으로 답변하세요.
{current_num}화 이후의 내용은 절대로 언급하지 마세요. (스포일러 방지)

작품 내용 ({current_num}화까지 회차별 요약):
{context}

답변 규칙:
- 위에 제공된 내용에 없는 정보는 "현재까지 읽으신 내용에서는 확인이 어렵습니다"라고 답하세요.
- 이모티콘/이모지는 절대 사용하지 마세요.
- 항상 한국어로 답변하세요.
- 간결하게 3~5문장 이내로 답변하세요."""

    history = "\n".join([
        f"{'사용자' if m.role == 'user' else 'AI'}: {m.content}"
        for m in messages[:-1]
    ])
    last_message = messages[-1].content
    prompt = f"{system_prompt}\n\n{history}\n사용자: {last_message}\nAI:"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        return ContentChatResponse(reply=response.text.strip())
    except Exception as e:
        print(f"Gemini 호출 오류: {e}")
        return ContentChatResponse(
            reply="일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        )
