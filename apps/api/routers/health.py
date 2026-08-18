"""Sağlık kontrolü endpoint'leri: /health/live ve /health/ready."""

import asyncpg
import redis.asyncio as redis
from fastapi import APIRouter, HTTPException, status

from apps.api.config.settings import settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def liveness() -> dict[str, str]:
    """Process ayakta mı? Hiçbir dış bağımlılığı kontrol etmez."""
    return {"status": "alive"}


@router.get("/ready")
async def readiness() -> dict[str, str]:
    """DB'ye ve Redis'e gerçekten bağlanıp bir komut çalıştırabiliyor muyuz?"""
    dsn = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    try:
        connection = await asyncpg.connect(dsn)
        try:
            await connection.fetchval("SELECT 1")
        finally:
            await connection.close()
    except (OSError, asyncpg.PostgresError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"database not ready: {exc}",
        ) from exc

    try:
        client = redis.from_url(settings.redis_url)
        try:
            # redis-py'nin ping() imzası **kwargs'ı tipsiz bırakmış (kütüphanenin
            # kendi eksiği) — bilerek görmezden geliyoruz, çalışma zamanını etkilemez.
            await client.ping()  # pyright: ignore[reportUnknownMemberType]
        finally:
            await client.aclose()
    except (OSError, redis.RedisError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"redis not ready: {exc}",
        ) from exc

    return {"status": "ready"}
