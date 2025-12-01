import logging
import os

from app.routes import embedder_endpoint
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.config import model
from app.service.security import API_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if API_TOKEN is None:
    logger.warning("API_TOKEN is not set.")
    exit(77)

_local_dir = os.path.dirname(__file__)

application = FastAPI(
    title="Local Embedder",
    docs_url='/docs'
)

# Mount static files - this is the key addition
html_dir = os.path.join(_local_dir, "html")
if os.path.exists(html_dir):
    application.mount("/static", StaticFiles(directory=html_dir), name="static")
    # Optionally, you can also mount it directly at root for convenience
    # application.mount("/", StaticFiles(directory=html_dir, html=True), name="html_files")

application.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

application.include_router(embedder_endpoint.router)


@application.get("/")
async def root(request: Request):
    # Get the Content-Type header
    content_type = request.headers.get("accept", "").lower()

    # Check if client wants HTML
    if not content_type or "text/html" in content_type or "html" in content_type:
        # Serve the HTML file from app/html folder
        html_file_path = Path(os.path.join(_local_dir, "html/index.html"))
        if html_file_path.exists():
            with open(html_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            return HTMLResponse(content=html_content)
        else:
            return HTMLResponse(
                content="<h1>Error: index.html not found</h1>",
                status_code=404
            )

    # Check if client wants JSON
    elif "application/json" in content_type or "json" in content_type:
        return JSONResponse(content={"model": model})

    # Default response (you can customize this)
    else:
        # Default to JSON if no specific content type is specified
        return JSONResponse(content={"model": model})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:application", host="0.0.0.0", port=5000, log_level="info")
