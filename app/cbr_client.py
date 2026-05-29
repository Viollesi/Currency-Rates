"""Client for the Central Bank of Russia currency rates."""

from datetime import date, datetime
import logging
import xml.etree.ElementTree as ET

import requests

from app.config import settings

logger = logging.getLogger(__name__)

SUPPORTED_CURRENCIES = {"USD", "EUR", "CNY", "GBP", "JPY"}


def fetch_rates_xml() -> str:
    """Fetch currency rates XML from CBR."""
    try:
        response = requests.get(settings.cbr_rates_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as error:
        logger.exception("Ошибка при запросе курсов валют в ЦБ РФ")
        message = "Не удалось получить курсы валют из ЦБ РФ"
        raise RuntimeError(message) from error

    return response.text


def parse_rates_xml(xml_text: str) -> tuple[date, list[dict]]:
    """Parse CBR XML and return rate date with supported currencies."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as error:
        logger.exception("Ошибка при разборе XML от ЦБ РФ")
        raise ValueError("Не удалось разобрать ответ ЦБ РФ") from error

    rate_date = _parse_rate_date(root.attrib.get("Date"))
    rates = []

    for currency in root.findall("Valute"):
        code = _get_text(currency, "CharCode")
        if code not in SUPPORTED_CURRENCIES:
            continue

        nominal = int(_get_text(currency, "Nominal"))
        cbr_value = _parse_float(_get_text(currency, "Value"))

        rates.append(
            {
                "code": code,
                "name": _get_text(currency, "Name"),
                "nominal": nominal,
                "value": round(cbr_value / nominal, 4),
                "rate_date": rate_date,
            },
        )

    if not rates:
        raise ValueError("В ответе ЦБ РФ не найдены нужные валюты")

    return rate_date, rates


def _parse_rate_date(value: str | None) -> date:
    if not value:
        raise ValueError("В ответе ЦБ РФ нет даты курса")

    return datetime.strptime(value, "%d.%m.%Y").date()


def _parse_float(value: str) -> float:
    return float(value.replace(",", "."))


def _get_text(currency: ET.Element, tag: str) -> str:
    element = currency.find(tag)
    if element is None or element.text is None:
        raise ValueError(f"В ответе ЦБ РФ нет поля {tag}")

    return element.text
