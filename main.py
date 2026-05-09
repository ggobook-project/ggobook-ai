import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import inspect_router
from routers import relay_router
from routers import novel_format_router
from routers import chatbot_router
from routers import parallel_universe_router
import os

app = FastAPI(title="GGoBook AI Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")],
    # 브라우저 보안정책으로 쿠키나 인증 정보를 안보내기 위해 사용
    # true로 설정하면 '쿠키랑 인증 정보도 같이 보내도 돼'라고 허용하는 것
    # 현재 꼬북이 챗봇을 로그인, 비로그인 나눠서 사용하는 기능은 안만들어서 
    # 일단 주석 처리 해놈.(나중을 위해서 남겨둠)
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기존 inspect_router 등록
app.include_router(inspect_router.router, prefix="/api")

# 🌟 2. 릴레이 라우터 등록
# (이전에 relay_router.py 내부에서 prefix="/api/relay"로 설정해두었으므로 그냥 연결만 하면 됩니다)
app.include_router(relay_router.router)
app.include_router(novel_format_router.router)
app.include_router(chatbot_router.router, prefix="/api")

# 평행우주 라우터 등록
app.include_router(parallel_universe_router.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "GGoBook AI 서버가 정상적으로 실행되었습니다!"}


@app.get("/ai/hello")
def say_hello():
    return {"message": "안녕하세요, 꼬북 AI입니다!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
