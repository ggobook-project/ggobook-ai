from pydantic import BaseModel


class NovelFormatRequest(BaseModel):
    text: str


class NovelFormatResponse(BaseModel):
    formatted_text: str
