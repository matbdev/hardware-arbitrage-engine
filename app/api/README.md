# API Package (`app/api/`)

FastAPI REST API application package for serving **Hardware Arbitrage Engine** Gold layer deal opportunities, market price baselines, price drop alerts, and trend analytics.

## Package Architecture

- **`main.py`**: Main FastAPI application instance (`app`), CORS middleware configuration, and global OpenAPI documentation metadata.
- **`deps.py`**: Injeção de dependências (`get_db()`) providing automatic SQLAlchemy database sessions with safe connection cleanup.
- **[`schemas/`](schemas/README.md)**: Pydantic V2 Response and Request Data Transfer Objects (DTOs).
- **[`v1/`](v1/README.md)**: Version 1 API router aggregation and resource endpoints.

## Execution & Serving

Run the development API server locally using `uv`:

```bash
uv run uvicorn app.api.main:app --reload
```

Interactive documentation is served at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Related Links
- [App Package Overview](../README.md)
- [API Schemas](schemas/README.md)
- [API V1 Router](v1/README.md)
- [App Services](../services/README.md)
- [App Models](../models/README.md)
