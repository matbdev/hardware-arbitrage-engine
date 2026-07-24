from app.models.gold import FactArbitrageOpportunity


def test_get_opportunities_endpoint_success(client, db_session):
    deal = FactArbitrageOpportunity(
        ad_id="ad-99",
        baseline_id="b1",
        title="Dell XPS 13",
        url="https://olx.com.br/99",
        current_price=2500.0,
        market_median_price=4000.0,
        potential_profit=1500.0,
        profit_margin_pct=0.375,
        opportunity_score=9.0,
        is_urgent_sale=False,
        item_condition="usado",
        specs_summary="i7, 16GB"
    )
    db_session.add(deal)
    db_session.commit()

    response = client.get("/api/v1/opportunities/?min_margin=0.10&page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["items"][0]["ad_id"] == "ad-99"


def test_get_opportunities_endpoint_invalid_query_returns_422(client):
    # min_margin exceeds le=1.0 constraint
    response = client.get("/api/v1/opportunities/?min_margin=5.0")
    assert response.status_code == 422
