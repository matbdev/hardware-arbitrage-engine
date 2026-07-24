# Hardware Arbitrage Engine

<p align="left">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.14-555555?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB" alt="Python 3.14" /></a>
  <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/badge/uv-Package_Manager-555555?style=for-the-badge&logo=uv&logoColor=white&labelColor=DE5FE9" alt="uv" /></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-REST_API-555555?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=009688" alt="FastAPI" /></a>
  <a href="https://www.uvicorn.org/"><img src="https://img.shields.io/badge/Uvicorn-ASGI_Server-555555?style=for-the-badge&logo=python&logoColor=white&labelColor=4B8BBE" alt="Uvicorn" /></a>
  <a href="https://swagger.io/"><img src="https://img.shields.io/badge/Swagger-OpenAPI_Docs-555555?style=for-the-badge&logo=swagger&logoColor=white&labelColor=85EA2D" alt="Swagger" /></a>
  <a href="https://docs.pytest.org/"><img src="https://img.shields.io/badge/Pytest-Testing-555555?style=for-the-badge&logo=pytest&logoColor=white&labelColor=0A9EDC" alt="Pytest" /></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-Database-555555?style=for-the-badge&logo=postgresql&logoColor=white&labelColor=4169E1" alt="PostgreSQL" /></a>
  <a href="https://alembic.sqlalchemy.org/"><img src="https://img.shields.io/badge/Alembic-Migrations-555555?style=for-the-badge&logo=sqlalchemy&logoColor=white&labelColor=6C757D" alt="Alembic" /></a>
  <a href="https://pola.rs/"><img src="https://img.shields.io/badge/Polars-Data_Engineering-555555?style=for-the-badge&logo=polars&logoColor=white&labelColor=CD7F32" alt="Polars" /></a>
  <a href="https://docs.pydantic.dev/"><img src="https://img.shields.io/badge/Pydantic-Validation-555555?style=for-the-badge&logo=pydantic&logoColor=white&labelColor=E91E63" alt="Pydantic" /></a>
  <a href="https://www.sqlalchemy.org/"><img src="https://img.shields.io/badge/SQLAlchemy-ORM-555555?style=for-the-badge&logo=sqlalchemy&logoColor=white&labelColor=D71F23" alt="SQLAlchemy" /></a>
  <a href="https://www.deepseek.com/"><img src="https://img.shields.io/badge/DeepSeek-AI_Appraiser-555555?style=for-the-badge&logo=openai&logoColor=white&labelColor=1D63ED" alt="DeepSeek AI" /></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/Ruff-Linter-555555?style=for-the-badge&logo=ruff&logoColor=black&labelColor=D7FF64" alt="Ruff" /></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Infrastructure-555555?style=for-the-badge&logo=docker&logoColor=white&labelColor=2496ED" alt="Docker" /></a>
</p>

## Project Overview
An asynchronous web scraping and AI evaluation pipeline designed to identify undervalued used electronics (e.g., Lenovo notebooks, Samsung Galaxy Books) in local classifieds and marketplaces. It combines a Medallion data architecture with an LLM-powered appraisal engine.

## Core Tech Stack
* **Package Management:** uv
* **Backend & API:** FastAPI, Uvicorn, httpx
* **Testing & Quality Assurance:** Pytest (Unit, Integration, and API endpoint testing)
* **Database & Migrations:** PostgreSQL (with SQLite support for dev) & Alembic (version-controlled schema migrations)
* **Data Validation:** Pydantic V2 (Response & Request DTO schemas)
* **Data Engineering / Processing:** Polars (Data transformation across Bronze, Silver, Gold layers)
* **ORM:** SQLAlchemy (with custom schema isolation for `bronze`, `silver`, and `gold` layers)
* **AI Integration:** DeepSeek V3 (via OpenRouter API)
* **Scraping:** BeautifulSoup4 / Playwright
* **Configuration:** YAML for search locations and scraping targets
* **Code Quality & Linting:** Ruff

## System Architecture
1. **The Scraper (Ingestion / Bronze Layer):** 
   * `httpx` to fetch live listings asynchronously.
   * Target metadata and search locations are loaded dynamically from `metadata/` YAML files.
   * Discovered links and extracted product details are persisted to Bronze layer database schema tables (`bronze.GeneralSearch` & `bronze.InformationExtraction`).
2. **The Processing Pipeline (Silver Layer):** 
   * `Polars` reads raw Bronze records.
   * Text cleaning, numeric specification extraction (RAM, CPU, storage), condition flag detection (`needs_repair`, `urgent_sale`), and one-hot encoding of product characteristics are saved to `silver.SilverCleanAd`.
3. **The AI Appraiser & Opportunities (Gold Layer):** 
   * Populates product dimensions (`gold.DimProduct`) first, computes market pricing baselines (`gold.FactMarketBaseline`), macro trends (`gold.FactMarketTrend`), and price drop alerts (`gold.FactPriceDropAlert`).
   * Evaluates deal opportunities against baselines and product spec summaries to calculate gross profit, margin %, and opportunity score (`gold.FactArbitrageOpportunity`).
4. **Database & Migration Layer:**
   * PostgreSQL database engine with custom schema namespaces (`bronze`, `silver`, `gold`).
   * `Alembic` manages environment database migrations and version control (`alembic revision --autogenerate`), replacing hardcoded schema initialization.
5. **API Serving Layer:**
   * FastAPI REST application serving Gold layer arbitrage deals, market baselines, price drop alerts, and trend analytics with generic pagination (`PaginatedResponse[T]`) and OpenAPI documentation (`/docs`).
6. **Testing & Quality Assurance:**
   * Automated 3-layer test suite (`tests/`) built with Pytest (unit cleaners/parsers, SQLite in-memory ORM service integration, and FastAPI `TestClient` endpoint tests).

## Folder Structure

```text
hardware-arbitrage-engine/
├── alembic/                     # Database migration environment & revision scripts
├── app/                         # Application core package
│   ├── api/                     # FastAPI application, DTO schemas & v1 REST endpoints
│   │   ├── main.py              # Application entry point & CORS configuration
│   │   ├── deps.py              # Database session dependency injection (get_db)
│   │   ├── schemas/             # Pydantic V2 DTO response & envelope schemas
│   │   └── v1/                  # Version 1 router & resource endpoints
│   │       ├── router.py        # Master v1 router aggregating all endpoints
│   │       └── endpoints/       # Route handlers (opportunities, baselines, trends, etc.)
│   ├── config.py                # Database connection, logging, and concurrency limits
│   ├── core/
│   │   └── deepseek_config.py   # DeepSeek AI API configuration
│   ├── models/                  # Layered SQLAlchemy ORM models (bronze, silver, gold schemas)
│   │   ├── base.py              # Base declarative model class
│   │   ├── bronze/              # GeneralSearch & InformationExtraction
│   │   ├── silver/              # SilverCleanAd
│   │   └── gold/                # DimProduct, FactMarketBaseline, FactMarketTrend, etc.
│   ├── pipelines/               # Production ETL execution modules
│   │   ├── runner.py            # Master pipeline orchestrator
│   │   ├── bronze/              # Bronze discovery & extraction (.py)
│   │   ├── silver/              # Silver cleaning & feature engineering (.py)
│   │   └── gold/                # Gold dimensions, baselines, trends & arbitrage (.py)
│   ├── scraper/                 # Resilient HTTP scraping engine
│   │   └── engine.py
│   ├── services/                # Database query services, marketplace parsers & crawlers
│   │   ├── opportunity_service.py
│   │   ├── baseline_service.py
│   │   ├── olx_service.py
│   │   └── crawlers/
│   └── utils/                   # Shared utility modules (pagination, db_helpers, httpx, YAML)
│       ├── pagination.py        # Generic offset calculation & response envelope helpers
│       ├── db_helpers.py        # Database count query helpers
│       ├── get_httpx_client.py
│       └── read_metadata.py
├── tests/                       # Automated Pytest quality assurance test suite
│   ├── conftest.py              # Shared fixtures (in-memory SQLite StaticPool & TestClient)
│   ├── unit/                    # Unit tests (cleaners, pagination, HTML parsing, schemas)
│   ├── integration/             # Service & ORM database integration tests
│   └── api/                     # FastAPI HTTP endpoint tests
├── notebooks/                   # Interactive Jupyter notebooks for experimentation
│   ├── bronze/                  # Discover & extraction notebooks
│   ├── silver/                  # Data cleaning notebook
│   └── gold/                    # Dimension, baseline, trend, and arbitrage notebooks
├── metadata/                    # Configuration as code (YAML)
│   ├── additional_info.yml
│   ├── scraping_targets.yml
│   └── search_locations.yml
├── docker-compose.yml           # Database infrastructure setup (PostgreSQL, Redis, Adminer)
├── main.py                      # Main entry point script
├── pyproject.toml               # project metadata and dependencies
└── uv.lock                      # Locked dependencies
```
