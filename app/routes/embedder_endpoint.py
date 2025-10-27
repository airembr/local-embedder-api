import logging
from time import time
from typing import List

from fastapi import APIRouter, Depends

from app.config import model
from app.service.embedder import get_embeddings, get_bm25
from app.service.security import verify_token

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(dependencies=[Depends(verify_token)])


def _convert(bm25):
    for item in bm25:
        item = item.as_object()
        item['values'] = item['values'].tolist()
        item['indices'] = item['indices'].tolist()
        yield item

@router.post("/embeddings")
async def embeddings(sentences: List[str], bm25: bool = False):
    t = time()
    embeddings = get_embeddings(sentences)
    if bm25:
        bm25 = get_bm25(sentences)
        bm25 = list(list(_convert(bm25)))
    else:
        bm25 = None

    return {"embeddings": {"sparse": bm25, "dense": embeddings.tolist()}, "model": model, "elapsed": time() - t}
