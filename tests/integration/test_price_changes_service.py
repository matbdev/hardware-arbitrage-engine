from app.models.gold import FactPriceDropAlert
from app.services.price_changes_service import get_changes


def test_get_price_changes_returns_paginated_alerts(db_session):
    alert = FactPriceDropAlert(
        ad_id="ad-100",
        title="Samsung Book i5",
        url="https://olx.com.br/vi/100",
        initial_price=2000.0,
        current_price=1600.0,
        price_change_pct=-0.20,
        days_on_market=10
    )
    db_session.add(alert)
    db_session.commit()

    result = get_changes(db_session, limit=10, page=1)
    assert result["total"] == 1
    assert result["items"][0].ad_id == "ad-100"
    assert result["items"][0].price_change_pct == -0.20
