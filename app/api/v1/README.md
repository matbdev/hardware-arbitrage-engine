# API Version 1 (`app/api/v1/`)

Manages Version 1 REST API route definitions, URL prefixing, and endpoint module aggregation under `/api/v1`.

## Submodules

- **`router.py`**: Master `api_router` instance (`APIRouter`). Aggregates and registers all v1 resource endpoint routers with tags and prefixes (`/health`, `/opportunities`, `/baselines`, `/price-changes`, `/products`, `/trends`).
- **[`endpoints/`](endpoints/README.md)**: Resource-specific HTTP route handler modules.

## Related Links
- [API Overview](../README.md)
- [API Schemas](../schemas/README.md)
- [API V1 Endpoints](endpoints/README.md)
- [App Services](../../services/README.md)
