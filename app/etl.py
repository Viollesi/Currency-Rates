"""Currency rates ETL pipeline."""

import logging
from typing import Any

from app.cbr_client import fetch_rates_xml, parse_rates_xml
from app.database import create_session
from app.redis_client import cache_latest_rates
from app.repositories import RateRepository, RawRateRepository

logger = logging.getLogger(__name__)


def extract_rates() -> str:
    """Extract currency rates XML."""
    logger.info("Запуск загрузки курсов валют из ЦБ РФ")
    return fetch_rates_xml()


def load_raw_rates(xml_text: str) -> list[dict[str, Any]]:
    """Save raw XML and return parsed rates."""
    rate_date, rates = parse_rates_xml(xml_text)

    with create_session() as session:
        RawRateRepository(session).save(rate_date=rate_date, raw_xml=xml_text)

    logger.info("Сырой ответ ЦБ РФ сохранен в PostgreSQL")
    return rates


def transform_rates(rates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Prepare rates for saving and caching."""
    logger.info("Курсы валют нормализованы")
    return rates


def save_rates(rates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Save normalized rates to PostgreSQL."""
    with create_session() as session:
        saved_rates = RateRepository(session).save_many(rates)

    logger.info(
        "Нормализованные курсы валют сохранены в PostgreSQL",
    )
    return [
        {
            "code": rate.code,
            "name": rate.name,
            "nominal": rate.nominal,
            "value": rate.value,
            "rate_date": rate.rate_date.isoformat(),
        }
        for rate in saved_rates
    ]


def cache_rates(rates: list[dict[str, Any]]) -> None:
    """Save latest rates to Redis."""
    cache_latest_rates(rates)


def run_pipeline() -> None:
    """Run full currency rates ETL pipeline."""
    logger.info("Старт ETL pipeline курсов валют")
    xml_text = extract_rates()
    parsed_rates = load_raw_rates(xml_text)
    rates = transform_rates(parsed_rates)
    saved_rates = save_rates(rates)
    cache_rates(saved_rates)
    logger.info("ETL pipeline курсов валют завершен")
