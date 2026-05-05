from fastapi import APIRouter
from models.parallel_universe_model import ParallelUniverseRequest, ParallelUniverseResponse
from services.parallel_universe_service import generate_parallel_universe

router = APIRouter()

@router.post("/parallel-universe", response_model=ParallelUniverseResponse)
async def parallel_universe(request: ParallelUniverseRequest):
    return generate_parallel_universe(request)