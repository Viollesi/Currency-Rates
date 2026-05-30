"""Database models."""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CurrencyRateRaw(Base):
    """Raw response from the Central Bank of Russia."""

    __tablename__ = "currency_rates_raw"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rate_date: Mapped[date] = mapped_column(Date, index=True)
    raw_xml: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class CurrencyRate(Base):
    """Normalized currency rate."""

    __tablename__ = "currency_rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(3), index=True)
    name: Mapped[str] = mapped_column(String(100))
    nominal: Mapped[int] = mapped_column(Integer)
    value: Mapped[float] = mapped_column(Float)
    rate_date: Mapped[date] = mapped_column(Date, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
