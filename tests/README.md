# Test Suite (`tests/`)

Automated quality assurance and test suite for the **Hardware Arbitrage Engine**, structured following Pytest conventions across Unit, Integration, and API testing layers.

## Submodules

- **[`unit/`](unit/README.md)**: Isolated unit tests for utility helpers, regex spec extractors, HTML parsers, and Pydantic schema validation.
- **[`integration/`](integration/README.md)**: Database and service layer integration tests using an in-memory SQLite database engine with attached schema namespaces (`bronze`, `silver`, `gold`).
- **[`api/`](api/README.md)**: FastAPI HTTP REST endpoint integration tests using `httpx.AsyncClient` / `TestClient`.
- **`conftest.py`**: Shared Pytest fixtures (`db_session`, `client`) configuring SQLite `StaticPool` and dependency overrides (`get_db`).

## Execution Protocol

Run the complete test suite locally using `uv`:

```bash
# Run all 28 tests
uv run pytest

# Run with verbose output
uv run pytest -v
```

## Related Links

- [App Package Overview](../app/README.md)
- [API Package](../app/api/README.md)
- [Services Package](../app/services/README.md)
- [Models Package](../app/models/README.md)
