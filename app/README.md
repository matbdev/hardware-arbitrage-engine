# App Package (`app/`)

Core application package for the **Hardware Arbitrage Engine**. Contains all business logic, data models, REST API endpoints, scraper services, ETL pipelines, and utilities.

## Package Architecture

- **[`api/`](api/README.md)**: FastAPI REST application, Pydantic DTO schemas, and v1 endpoints.
- **[`core/`](core/README.md)**: DeepSeek AI model integration and configuration settings.
- **[`models/`](models/README.md)**: SQLAlchemy ORM schema definitions organized by layer ([`bronze`](models/bronze/README.md), [`silver`](models/silver/README.md), [`gold`](models/gold/README.md)).
- **[`pipelines/`](pipelines/README.md)**: Production ETL pipeline runners for data ingestion, cleaning, and market evaluation.
- **[`scraper/`](scraper/README.md)**: Async HTTP scraping engine with retry policies and rate limiting.
- **[`services/`](services/README.md)**: Marketplace crawlers, query services, and HTML parsing services.
- **[`utils/`](utils/README.md)**: Shared utility functions for pagination, database helpers, HTTP clients, and YAML metadata parsing.
- **`config.py`**: Centralized SQLite/PostgreSQL engine initialization and database configuration.
