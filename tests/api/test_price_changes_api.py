from app.models.gold import FactPriceDropAlert


def test_get_price_changes_endpoint_returns_paginated_response(client, db_session):
    alert = FactPriceDropAlert(
        ad_id="ad-50",
        title="MacBook Air M1",
        url="https://olx.com.br/vi/50",
        initial_price=5000.0,
        current_price=4200.0,
        price_change_pct=-0.16,
        days_on_market=7
    )
    db_session.add(alert)
    db_session.commit()

    response = client.get("/api/v1/price-changes/?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["ad_id"] == "ad-50"
    assert data["items"][0]["price_change_pct"] == -0.16
