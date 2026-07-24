from datetime import date

from app.models.gold import FactMarketTrend
from app.services.trends_service import get_market_trends_by_category


def test_get_market_trends_by_category_returns_trend(db_session):
    trend = FactMarketTrend(
        id=1,
        date=date(2026, 7, 24),
        category="notebook",
        brand="Lenovo",
        median_market_price=2600.0,
        total_volume_available=120
    )
    db_session.add(trend)
    db_session.commit()

    result = get_market_trends_by_category(db_session, category="notebook")
    assert result is not None
    assert result.category == "notebook"
    assert result.median_market_price == 2600.0


def test_get_market_trends_by_category_returns_none_for_missing(db_session):
    result = get_market_trends_by_category(db_session, category="smartphone")
    assert result is None
