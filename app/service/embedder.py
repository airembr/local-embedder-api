from typing import List

from sentence_transformers import SentenceTransformer
from fastembed.sparse.bm25 import Bm25
from app.config import model

dense_embedder = SentenceTransformer(model)
bm25_embedder = Bm25('Qdrant/bm25')

def get_embeddings(sentences: List[str], normalize: bool = False):
    return dense_embedder.encode(sentences, show_progress_bar=False, normalize_embeddings=normalize)


def get_bm25(sentences: List[str]):
    return bm25_embedder.passage_embed(sentences)
