"""FastAPI entrypoint."""

import logging
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_session
from app.models import CurrencyRate
from app.redis_client import get_cached_rates
from app.repositories import RateRepository

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)


@app.get("/health")
def health() -> dict[str, str]:
    """Check that the API is running."""
    return {"status": "ok"}


@app.get("/rates")
def get_rates(session: Session = Depends(get_session)) -> dict[str, list[dict[str, Any]]]:
    """Get latest currency rates."""
    rates = _get_rates_from_cache()
    if not rates:
        db_rates = RateRepository(session).get_latest_rates()
        rates = [_rate_to_dict(rate) for rate in db_rates]

    if not rates:
        raise HTTPException(
            status_code=404,
            detail="Курсы валют еще не загружены",
        )

    return {"rates": rates}


@app.get("/rates/{code}")
def get_rate_by_code(
    code: str,
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    """Get latest currency rate by code."""
    currency_code = code.upper()
    cached_rates = _get_rates_from_cache()

    for rate in cached_rates:
        if rate["code"] == currency_code:
            return rate

    db_rate = RateRepository(session).get_latest_by_code(currency_code)
    if db_rate is None:
        raise HTTPException(
            status_code=404,
            detail=f"Курс валюты {currency_code} не найден",
        )

    return _rate_to_dict(db_rate)


def _get_rates_from_cache() -> list[dict[str, Any]]:
    try:
        return get_cached_rates()
    except RuntimeError:
        logger.warning("Не удалось прочитать курсы из Redis, читаем из PostgreSQL")
        return []


def _rate_to_dict(rate: CurrencyRate) -> dict[str, Any]:
    return {
        "code": rate.code,
        "name": rate.name,
        "nominal": rate.nominal,
        "value": rate.value,
        "rate_date": rate.rate_date.isoformat(),
    }
