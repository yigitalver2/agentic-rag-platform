"""FastAPI uygulamasının giriş noktası."""

from fastapi import FastAPI

from apps.api.routers import health

app = FastAPI(title="Agentic RAG Platform API")

app.include_router(health.router)
