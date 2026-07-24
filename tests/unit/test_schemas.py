import pytest
from pydantic import ValidationError

from app.api.schemas import ArbitrageOpportunity


def test_arbitrage_opportunity_optional_image_allows_none():
    data = {
        "ad_id": "olx-12345",
        "baseline_id": "lenovo_i7_16gb",
        "title": "Lenovo ThinkPad",
        "url": "https://olx.com.br/vi/12345",
        "first_image_src": None,
        "item_condition": "usado",
        "specs_summary": "i7, 16GB",
        "is_urgent_sale": False,
        "current_price": 1500.0,
        "market_median_price": 2200.0,
        "potential_profit": 700.0,
        "profit_margin_pct": 0.318,
        "opportunity_score": 8.5,
    }
    opportunity = ArbitrageOpportunity(**data)
    assert opportunity.first_image_src is None
    assert opportunity.ad_id == "olx-12345"


def test_arbitrage_opportunity_invalid_price_raises_validation_error():
    data = {
        "ad_id": "olx-12345",
        "baseline_id": "lenovo_i7_16gb",
        "title": "Lenovo ThinkPad",
        "url": "https://olx.com.br/vi/12345",
        "first_image_src": None,
        "item_condition": "usado",
        "specs_summary": "i7, 16GB",
        "is_urgent_sale": False,
        "current_price": "invalid_price_string",  # Invalid type
        "market_median_price": 2200.0,
        "potential_profit": 700.0,
        "profit_margin_pct": 0.318,
        "opportunity_score": 8.5,
    }
    with pytest.raises(ValidationError):
        ArbitrageOpportunity(**data)
