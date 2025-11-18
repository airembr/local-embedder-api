import logging
from collections import OrderedDict
from time import time
from typing import List, Dict

from fastapi import APIRouter, Depends

from app.config import model
from app.service.embedder import get_embeddings, get_bm25
from app.service.security import verify_token

from sdk.airembr.model.embedding.embedding import EmbeddingResponse

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
async def embeddings(texts: OrderedDict[str, str], bm25: bool = False):
    t = time()

    relations = list(texts.keys())
    values = list(texts.values())

    embeddings = get_embeddings(values)
    embeddings = embeddings.tolist()

    if embeddings:
        embeddings = list(zip(relations, embeddings))

    if bm25:
        bm25 = get_bm25(values)
        bm25 = list(list(_convert(bm25)))
        bm25 = list(zip(relations, bm25))
    else:
        bm25 = None
    elapsed = time() - t

    logger.info(f"Vectors: {len(embeddings)}, Elapsed time: {elapsed}")
    return EmbeddingResponse(sparse=bm25, dense=embeddings, model=model, elapsed=elapsed)
