# Running with Docker

The Local Embedder API is published on Docker Hub as:

```
tracardi/airembr-os-hf-768-embedding-api:0.0.2
```

## Pull the image

```bash
docker pull tracardi/airembr-os-hf-768-embedding-api:0.0.2
```

## Environment variables

| Variable          | Required | Default                             | Description                                                                 |
|--------------------|----------|--------------------------------------|-------------------------------------------------------------------------------|
| `API_TOKEN`         | Yes      | —                                    | Bearer token clients must supply to call the API. The container exits (code 77) at startup if this is not set. |
| `EMBEDDING_MODEL`   | No       | `intfloat/multilingual-e5-base`      | SentenceTransformer model used to compute dense embeddings (768 dimensions). |

## Run

```bash
docker run -d \
  --name local-embedder-api \
  -p 5000:5000 \
  -e API_TOKEN="change-me" \
  -e EMBEDDING_MODEL="intfloat/multilingual-e5-base" \
  tracardi/airembr-os-hf-768-embedding-api:0.0.2
```

The API will be available at `http://localhost:5000`, with interactive Swagger docs at `http://localhost:5000/docs`.

## Run with Docker Compose

```yaml
services:
  local-embedder-api:
    image: tracardi/airembr-os-hf-768-embedding-api:0.0.2
    ports:
      - "5000:5000"
    environment:
      API_TOKEN: "change-me"
      EMBEDDING_MODEL: "intfloat/multilingual-e5-base"
```

```bash
docker compose up -d
```

## Verify it's running

```bash
curl -H "Authorization: Bearer change-me" \
     -H "Content-Type: application/json" \
     -X PUT "http://localhost:5000/embeddings" \
     -d '["hello world"]'
```

See [README.md](README.md) for full API documentation.
