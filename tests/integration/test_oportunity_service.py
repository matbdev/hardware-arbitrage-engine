from app.models.gold import FactArbitrageOpportunity
from app.services.opportunity_service import get_top_deals


def test_get_top_deals_filters_by_minimum_margin(db_session):
    # Seed mock data into test database
    deal_high_roi = FactArbitrageOpportunity(
        ad_id="ad-1",
        baseline_id="b1",
        title="High Margin Deal",
        url="https://olx.com.br/1",
        current_price=1000.0,
        market_median_price=2000.0,
        potential_profit=1000.0,
        profit_margin_pct=0.50, # 50% margin
        opportunity_score=9.5,
        is_urgent_sale=True,
        item_condition="usado",
        specs_summary="i7, 16GB"
    )
    deal_low_roi = FactArbitrageOpportunity(
        ad_id="ad-2",
        baseline_id="b1",
        title="Low Margin Deal",
        url="https://olx.com.br/2",
        current_price=1900.0,
        market_median_price=2000.0,
        potential_profit=100.0,
        profit_margin_pct=0.05, # 5% margin
        opportunity_score=3.0,
        is_urgent_sale=False,
        item_condition="usado",
        specs_summary="i5, 8GB"
    )
    db_session.add_all([deal_high_roi, deal_low_roi])
    db_session.commit()

    # Query service with min_margin = 0.20 (20%)
    result = get_top_deals(db=db_session, min_margin=0.20, limit=10, page=1)

    # Verify only high margin deal is returned
    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0].ad_id == "ad-1"