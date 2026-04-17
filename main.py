from fastapi import FastAPI
from routers import inspect_router

app = FastAPI()

# 2. inspect_router를 등록합니다. prefix는 "/api"로 설정합니다.
app.include_router(inspect_router.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "GGoBook AI 서버가 정상적으로 실행되었습니다!"}


@app.get("/ai/hello")
def say_hello():
    return {"message": "안녕하세요, 꼬북 AI입니다!"}
