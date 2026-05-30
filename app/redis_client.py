"""Redis helper functions."""

import json
import logging
from typing import Any

import redis

from app.config import settings

logger = logging.getLogger(__name__)

LATEST_RATES_KEY = "latest_rates"


def get_redis_client() -> redis.Redis:
    """Create Redis client."""
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True,
    )


def cache_latest_rates(rates: list[dict[str, Any]]) -> None:
    """Save latest rates to Redis."""
    client = get_redis_client()
    try:
        client.set(LATEST_RATES_KEY, json.dumps(rates, default=str))
        logger.info("Последние курсы валют сохранены в Redis")
    except redis.RedisError as error:
        logger.exception(
            "Ошибка при сохранении курсов валют в Redis",
        )
        message = "Не удалось сохранить курсы валют в Redis"
        raise RuntimeError(message) from error


def get_cached_rates() -> list[dict[str, Any]]:
    """Get latest rates from Redis."""
    client = get_redis_client()
    try:
        value = client.get(LATEST_RATES_KEY)
    except redis.RedisError as error:
        logger.exception("Ошибка при чтении курсов валют из Redis")
        message = "Не удалось прочитать курсы валют из Redis"
        raise RuntimeError(message) from error

    if value is None:
        return []

    return json.loads(value)
