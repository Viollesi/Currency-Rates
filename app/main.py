"""FastAPI entrypoint."""

from fastapi import FastAPI

from app.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/health")
def health() -> dict[str, str]:
    """Check that the API is running."""
    return {"status": "ok"}
