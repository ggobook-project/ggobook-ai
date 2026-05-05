import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import inspect_router
from routers import relay_router
from routers import novel_format_router
from routers import chatbot_router

app = FastAPI(title="GGoBook AI Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기존 inspect_router 등록
app.include_router(inspect_router.router, prefix="/api")

# 🌟 2. 릴레이 라우터 등록
# (이전에 relay_router.py 내부에서 prefix="/api/relay"로 설정해두었으므로 그냥 연결만 하면 됩니다)
app.include_router(relay_router.router)
app.include_router(novel_format_router.router)
app.include_router(chatbot_router.router)


@app.get("/")
def read_root():
    return {"message": "GGoBook AI 서버가 정상적으로 실행되었습니다!"}


@app.get("/ai/hello")
def say_hello():
    return {"message": "안녕하세요, 꼬북 AI입니다!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
