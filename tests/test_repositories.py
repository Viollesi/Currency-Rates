"""Tests for repositories."""

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.repositories import RateRepository


def test_get_latest_rates_returns_rates_for_latest_date() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    with session_factory() as session:
        repository = RateRepository(session)
        repository.save_many(
            [
                {
                    "code": "USD",
                    "name": "Доллар США",
                    "nominal": 1,
                    "value": 90.0,
                    "rate_date": date(2026, 5, 29),
                },
                {
                    "code": "EUR",
                    "name": "Евро",
                    "nominal": 1,
                    "value": 98.0,
                    "rate_date": date(2026, 5, 30),
                },
            ],
        )

        rates = repository.get_latest_rates()

    assert len(rates) == 1
    assert rates[0].code == "EUR"
