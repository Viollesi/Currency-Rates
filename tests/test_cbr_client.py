"""Tests for CBR client."""

from app.cbr_client import parse_rates_xml


def test_parse_rates_xml_filters_and_normalizes_supported_rates() -> None:
    xml_text = """
    <ValCurs Date="30.05.2026" name="Foreign Currency Market">
        <Valute ID="R01235">
            <NumCode>840</NumCode>
            <CharCode>USD</CharCode>
            <Nominal>1</Nominal>
            <Name>Доллар США</Name>
            <Value>90,1234</Value>
        </Valute>
        <Valute ID="R01375">
            <NumCode>156</NumCode>
            <CharCode>CNY</CharCode>
            <Nominal>10</Nominal>
            <Name>Китайский юань</Name>
            <Value>125,0000</Value>
        </Valute>
        <Valute ID="R00000">
            <NumCode>000</NumCode>
            <CharCode>AAA</CharCode>
            <Nominal>1</Nominal>
            <Name>Тестовая валюта</Name>
            <Value>1,0000</Value>
        </Valute>
    </ValCurs>
    """

    rate_date, rates = parse_rates_xml(xml_text)

    assert rate_date.isoformat() == "2026-05-30"
    assert len(rates) == 2
    assert rates[0]["code"] == "USD"
    assert rates[0]["value"] == 90.1234
    assert rates[1]["code"] == "CNY"
    assert rates[1]["value"] == 12.5
