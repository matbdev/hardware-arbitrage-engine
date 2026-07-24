from datetime import date

from app.models.gold import FactMarketBaseline
from app.services.baseline_service import get_baseline_by_id


def test_get_baseline_by_id_returns_correct_record(db_session):
    baseline = FactMarketBaseline(
        id=1,
        baseline_id="lenovo_i7_16gb_512gb",
        category="notebook",
        cpu_brand="Intel",
        ram_gb=16,
        storage_gb=512,
        active_ads_count=10,
        min_price=1500.0,
        median_price=2500.0,
        max_price=3500.0,
        last_recalculated_at=date(2026, 7, 24)
    )
    db_session.add(baseline)
    db_session.commit()

    result = get_baseline_by_id(db_session, baseline_id="lenovo_i7_16gb_512gb")
    assert result is not None
    assert result.baseline_id == "lenovo_i7_16gb_512gb"
    assert result.median_price == 2500.0


def test_get_baseline_by_id_returns_none_if_not_found(db_session):
    result = get_baseline_by_id(db_session, baseline_id="non_existent_id")
    assert result is None
