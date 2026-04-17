from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "GGoBook AI 서버가 정상적으로 실행되었습니다!"}


@app.get("/ai/hello")
def say_hello():
    return {"message": "안녕하세요, 꼬북 AI입니다!"}
