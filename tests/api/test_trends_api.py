from datetime import date

from app.models.gold import FactMarketTrend


def test_get_trends_endpoint_not_found_returns_404(client):
    response = client.get("/api/v1/trends/?category=non_existent_category")
    assert response.status_code == 404
    assert "No trend record found" in response.json()["detail"]


def test_get_trends_endpoint_success_returns_200(client, db_session):
    trend = FactMarketTrend(
        id=1,
        date=date(2026, 7, 24),
        category="notebook",
        brand="Apple",
        median_market_price=5500.0,
        total_volume_available=45
    )
    db_session.add(trend)
    db_session.commit()

    response = client.get("/api/v1/trends/?category=notebook")
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "notebook"
    assert data["brand"] == "Apple"
    assert data["median_market_price"] == 5500.0
