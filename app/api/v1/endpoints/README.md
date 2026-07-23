# API V1 Endpoints (`app/api/v1/endpoints/`)

Contains resource-specific HTTP route handler modules for Version 1 of the REST API.

## Resource Endpoints

- **`health.py`**:
  - `GET /api/v1/health/live`: Application liveness check.
  - `GET /api/v1/health/ready`: Database connectivity readiness check (`SELECT 1`).
- **`opportunities.py`**:
  - `GET /api/v1/opportunities`: Returns paginated high-ROI deal opportunities (`PaginatedResponse[ArbitrageOpportunity]`).
- **`baselines.py`**:
  - `GET /api/v1/baselines`: Returns market benchmark price statistics (`MarketBaseline`).
- **`price_changes.py`**:
  - `GET /api/v1/price-changes`: Returns paginated price reduction alerts (`PaginatedResponse[PriceChangesAlert]`).
- **`products.py`**:
  - `GET /api/v1/products`: Returns paginated hardware product dimensions (`PaginatedResponse[Product]`).
- **`trends.py`**:
  - `GET /api/v1/trends`: Returns market price trend analytics by category (`MarketTrend`).

## Related Links
- [API V1 Router](../README.md)
- [API Overview](../../README.md)
- [API Schemas](../../schemas/README.md)
- [App Services](../../../services/README.md)
