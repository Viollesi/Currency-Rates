"""Simple repositories for currency rates."""

from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CurrencyRate, CurrencyRateRaw


class RawRateRepository:
    """Repository for raw currency rate responses."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, rate_date: date, raw_xml: str) -> CurrencyRateRaw:
        """Save raw XML response."""
        raw_rate = CurrencyRateRaw(rate_date=rate_date, raw_xml=raw_xml)
        self.session.add(raw_rate)
        self.session.commit()
        self.session.refresh(raw_rate)
        return raw_rate


class RateRepository:
    """Repository for normalized currency rates."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def save_many(self, rates: list[dict[str, Any]]) -> list[CurrencyRate]:
        """Save list of normalized rates."""
        rate_models = [CurrencyRate(**rate) for rate in rates]
        self.session.add_all(rate_models)
        self.session.commit()

        for rate_model in rate_models:
            self.session.refresh(rate_model)

        return rate_models

    def get_latest_rates(self) -> list[CurrencyRate]:
        """Get latest rates by max available date."""
        latest_date = self.session.scalar(
            select(CurrencyRate.rate_date).order_by(CurrencyRate.rate_date.desc()),
        )
        if latest_date is None:
            return []

        query = (
            select(CurrencyRate)
            .where(CurrencyRate.rate_date == latest_date)
            .order_by(CurrencyRate.code)
        )
        return list(self.session.scalars(query).all())

    def get_latest_by_code(self, code: str) -> CurrencyRate | None:
        """Get latest currency rate by code."""
        query = (
            select(CurrencyRate)
            .where(CurrencyRate.code == code.upper())
            .order_by(CurrencyRate.rate_date.desc(), CurrencyRate.created_at.desc())
        )
        return self.session.scalar(query)
