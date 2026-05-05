from pydantic import BaseModel
from typing import Optional

class ParallelUniverseRequest(BaseModel):
    title: str
    summary: str
    content_text: str
    what_if: str

class ParallelUniverseResponse(BaseModel):
    parallel_universe_text: str