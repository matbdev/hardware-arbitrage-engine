from datetime import date

from app.models.gold import FactMarketBaseline


def test_get_baselines_endpoint_not_found_returns_404(client):
    response = client.get("/api/v1/baselines/?baseline_id=unknown_id")
    assert response.status_code == 404
    assert "No baseline record found" in response.json()["detail"]


def test_get_baselines_endpoint_success_returns_200(client, db_session):
    baseline = FactMarketBaseline(
        id=1,
        baseline_id="lenovo_i7_16gb",
        category="notebook",
        cpu_brand="Intel",
        ram_gb=16,
        storage_gb=512,
        active_ads_count=12,
        min_price=1800.0,
        median_price=2600.0,
        max_price=3500.0,
        last_recalculated_at=date(2026, 7, 24)
    )
    db_session.add(baseline)
    db_session.commit()

    response = client.get("/api/v1/baselines/?baseline_id=lenovo_i7_16gb")
    assert response.status_code == 200
    data = response.json()
    assert data["baseline_id"] == "lenovo_i7_16gb"
    assert data["median_price"] == 2600.0
