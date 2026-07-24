# API Endpoint Tests (`tests/api/`)

Contains HTTP integration tests for FastAPI REST API endpoints using FastAPI's `TestClient` and `client` fixture.

## Test Components

- **`test_health.py`**: Tests `GET /api/v1/health/live` (liveness) and `GET /api/v1/health/ready` (database connectivity).
- **`test_opportunities_api.py`**: Tests `GET /api/v1/opportunities/` filtering by `min_margin` & `max_price`, checking `200 OK` paginated JSON responses and `422 Unprocessable Entity` validation errors.
- **`test_baselines_api.py`**: Tests `GET /api/v1/baselines/` checking `200 OK` for existing baseline IDs and `404 Not Found` for missing IDs.
- **`test_trends_api.py`**: Tests `GET /api/v1/trends/` checking `200 OK` for valid category trends and `404 Not Found` for unknown categories.
- **`test_products_api.py`**: Tests `GET /api/v1/products/` checking `200 OK` paginated responses.
- **`test_price_changes_api.py`**: Tests `GET /api/v1/price-changes/` checking `200 OK` price reduction alert responses.

## Execution

```bash
uv run pytest tests/api/
```

## Related Links

- [Test Suite Overview](../README.md)
- [Unit Tests](../unit/README.md)
- [Integration Tests](../integration/README.md)
- [API V1 Router](../../app/api/v1/README.md)
- [API V1 Endpoints](../../app/api/v1/endpoints/README.md)
