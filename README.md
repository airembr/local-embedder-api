# Local Embedder API

A small FastAPI service that generates dense (sentence-transformer) and optional sparse (BM25) embeddings locally, without calling any external API.

## Requirements

- Python 3.12+
- The `airembr` SDK available on the Python path (provides `EmbeddingResponse`, imported in `app/routes/embedder_endpoint.py`)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
```

## Configuration

The service is configured entirely through environment variables.

| Variable          | Required | Default                             | Description                                                                 |
|--------------------|----------|--------------------------------------|-------------------------------------------------------------------------------|
| `API_TOKEN`         | Yes      | —                                    | Bearer token clients must supply to call the API. The service refuses to start (exit code 77) if this is not set. |
| `EMBEDDING_MODEL`   | No       | `intfloat/multilingual-e5-base`      | SentenceTransformer model used to compute dense embeddings (768 dimensions). |

```bash
export API_TOKEN="change-me"
export EMBEDDING_MODEL="intfloat/multilingual-e5-base"
```

## Running

```bash
python -m app.main
```

or with `uvicorn` directly:

```bash
uvicorn app.main:application --host 0.0.0.0 --port 5000
```

The API will be available at `http://localhost:5000`, with interactive Swagger docs at `http://localhost:5000/docs`.

## Authentication

All `/embeddings` endpoints require a Bearer token that matches `API_TOKEN`:

```
Authorization: Bearer <API_TOKEN>
```

## Endpoints

### `GET /`

Returns a small HTML landing page (if `Accept: text/html`) or `{"model": "<embedding model name>"}` as JSON otherwise. No authentication required.

### `POST /embeddings`

Computes embeddings for a keyed set of texts and returns both the vectors and, optionally, BM25 sparse vectors.

**Query parameters**

| Name        | Type | Default | Description                                  |
|-------------|------|---------|-----------------------------------------------|
| `bm25`      | bool | `false` | Also compute BM25 sparse embeddings.          |
| `normalize` | bool | `false` | L2-normalize the dense embedding vectors.     |

**Body** — a JSON object mapping arbitrary keys to text:

```json
{
  "doc1": "The quick brown fox jumps over the lazy dog.",
  "doc2": "Local embeddings without an external API."
}
```

**Response**

```json
{
  "sparse": null,
  "dense": {
    "doc1": [0.0123, -0.0456, ...],
    "doc2": [0.0789, 0.0011, ...]
  },
  "model": "intfloat/multilingual-e5-base",
  "elapsed": 0.0421
}
```

**Example**

```bash
curl -X POST "http://localhost:5000/embeddings?bm25=true&normalize=true" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"doc1": "The quick brown fox jumps over the lazy dog."}'
```

### `PUT /embeddings`

Computes dense embeddings for a plain list of texts, returned in the same order as the input.

**Query parameters**

| Name        | Type | Default | Description                              |
|-------------|------|---------|--------------------------------------------|
| `normalize` | bool | `false` | L2-normalize the dense embedding vectors. |

**Body** — a JSON array of strings:

```json
["The quick brown fox jumps over the lazy dog.", "Local embeddings without an external API."]
```

**Response** — a JSON array of embedding vectors, in the same order:

```json
[
  [0.0123, -0.0456, ...],
  [0.0789, 0.0011, ...]
]
```

**Example**

```bash
curl -X PUT "http://localhost:5000/embeddings?normalize=true" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '["The quick brown fox jumps over the lazy dog."]'
```
