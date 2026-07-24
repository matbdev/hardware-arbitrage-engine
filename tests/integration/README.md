# Integration Tests (`tests/integration/`)

Contains database and service layer integration tests that verify SQLAlchemy ORM queries, filtering, sorting, and pagination logic against an in-memory database engine.

## Test Components

- **`test_oportunity_service.py`**: Tests `get_top_deals` filtering by `min_margin` and `max_price`, sorting by `opportunity_score.desc()`.
- **`test_baseline_service.py`**: Tests `get_baseline_by_id` querying `FactMarketBaseline` records.
- **`test_trends_service.py`**: Tests `get_market_trends_by_category` querying `FactMarketTrend` records.
- **`test_product_service.py`**: Tests `get_products_by_baseline_id` querying `DimProduct` dimension records.
- **`test_price_changes_service.py`**: Tests `get_changes` querying `FactPriceDropAlert` alert records.

## Fixture & Database Setup

Tests utilize the `db_session` fixture defined in `tests/conftest.py`. The fixture builds SQLite in-memory database tables with schema attachments (`ATTACH DATABASE ':memory:' AS bronze/silver/gold`) to ensure multi-schema SQLAlchemy model compatibility.

## Execution

```bash
uv run pytest tests/integration/
```

## Related Links

- [Test Suite Overview](../README.md)
- [Unit Tests](../unit/README.md)
- [API Endpoint Tests](../api/README.md)
- [App Services](../../app/services/README.md)
- [Gold Models](../../app/models/gold/README.md)
