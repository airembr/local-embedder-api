from time import time

from sentence_transformers import SentenceTransformer

from app.config import model

dense_embedder = SentenceTransformer(model)


def get_embeddings(sentences):
    t = time()
    embeddings = dense_embedder.encode(sentences, show_progress_bar=False)
    elapsed = time() - t
    return embeddings, elapsed
