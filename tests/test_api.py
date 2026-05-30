"""Tests for FastAPI endpoints."""

from collections.abc import Generator

from fastapi.testclient import TestClient

from app.database import get_session
from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_rate_by_code_from_cache(monkeypatch) -> None:
    def fake_session() -> Generator[None, None, None]:
        yield None

    monkeypatch.setattr(
        "app.main.get_cached_rates",
        lambda: [
            {
                "code": "USD",
                "name": "Доллар США",
                "nominal": 1,
                "value": 90.12,
                "rate_date": "2026-05-30",
            },
        ],
    )
    app.dependency_overrides[get_session] = fake_session

    response = client.get("/rates/USD")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["code"] == "USD"


def test_get_rate_by_code_not_found(monkeypatch) -> None:
    class FakeRateRepository:
        def __init__(self, session) -> None:
            self.session = session

        def get_latest_by_code(self, code: str):
            return None

    def fake_session() -> Generator[None, None, None]:
        yield None

    monkeypatch.setattr("app.main.get_cached_rates", lambda: [])
    monkeypatch.setattr("app.main.RateRepository", FakeRateRepository)
    app.dependency_overrides[get_session] = fake_session

    response = client.get("/rates/ABC")

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["detail"] == "Курс валюты ABC не найден"
