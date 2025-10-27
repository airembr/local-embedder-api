import logging
from typing import List

from fastapi import APIRouter, Depends

from app.config import model
from app.service.embedder import get_embeddings
from app.service.security import verify_token

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(dependencies=[Depends(verify_token)])


@router.post("/embeddings")
async def embeddings(sentences: List[str]):
    result, elapsed = get_embeddings(sentences)
    return {"embeddings": result.tolist(), "model": model, "elapsed": elapsed}
