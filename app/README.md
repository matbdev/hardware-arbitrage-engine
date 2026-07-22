# App Package (`app/`)

Core application package for the **Hardware Arbitrage Engine**. Contains all business logic, data models, scraper services, ETL pipelines, and utilities.

## Package Architecture

- **[`core/`](core/README.md)**: DeepSeek AI model integration and configuration settings.
- **[`models/`](models/README.md)**: SQLAlchemy ORM schema definitions organized by layer ([`bronze`](models/bronze/README.md), [`silver`](models/silver/README.md), [`gold`](models/gold/README.md)).
- **[`pipelines/`](pipelines/README.md)**: Production ETL pipeline runners for data ingestion, cleaning, and market evaluation.
- **[`scraper/`](scraper/README.md)**: Async HTTP scraping engine with retry policies and rate limiting.
- **[`services/`](services/README.md)**: Marketplace crawlers and HTML parsing services.
- **[`utils/`](utils/README.md)**: Shared utility functions for HTTP clients and YAML metadata parsing.
- **`config.py`**: Centralized SQLite/PostgreSQL engine initialization and database configuration.
