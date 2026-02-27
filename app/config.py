import os

# model = 'paraphrase-multilingual-MiniLM-L12-v2'
model = os.environ.get("EMBEDDING_MODEL", 'intfloat/multilingual-e5-base')
# model = 'BAAI/bge-m3'