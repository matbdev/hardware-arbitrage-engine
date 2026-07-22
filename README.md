# Hardware Arbitrage Engine

<p align="left">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.14-555555?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB" alt="Python 3.14" /></a>
  <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/badge/uv-Package_Manager-555555?style=for-the-badge&logo=uv&logoColor=white&labelColor=DE5FE9" alt="uv" /></a>
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
* **Backend & API:** httpx
* **Data Validation:** Pydantic (Strict schema enforcement for AI outputs)
* **Data Engineering / Processing:** Polars (Data transformation across Bronze, Silver, Gold layers)
* **ORM & Database:** SQLAlchemy / SQLite (PostgreSQL ready for production)
* **AI Integration:** DeepSeek V3 (via OpenRouter API)
* **Scraping:** BeautifulSoup4 / Playwright
* **Configuration:** YAML for search locations and scraping targets
* **Code Quality:** Ruff

## System Architecture
1. **The Scraper (Ingestion / Bronze Layer):** 
   * `httpx` to fetch live listings asynchronously.
   * Target metadata and search locations are loaded dynamically from `metadata/` YAML files.
   * Discovered links and extracted product details are persisted to the Bronze layer tables (`GeneralSearch` & `InformationExtraction`).
2. **The Processing Pipeline (Silver Layer):** 
   * `Polars` reads raw Bronze records.
   * Text cleaning, numeric specification extraction (RAM, CPU, storage), condition flag detection (`needs_repair`, `urgent_sale`), and one-hot encoding of product characteristics are saved to `SilverCleanAd`.
3. **The AI Appraiser & Opportunities (Gold Layer):** 
   * Evaluates cost-benefit ratios, market baselines, price drop alerts, and arbitrage deals.
4. **Serving:**
   * Profitable arbitrage opportunities are served via API endpoints or dashboard interface.

## Folder Structure

```text
hardware-arbitrage-engine/
├── app/                         # Application core package
│   ├── config.py                # Database connection, logging, and concurrency limits
│   ├── core/
│   │   └── deepseek_config.py   # DeepSeek AI API configuration
│   ├── models/                  # SQLAlchemy ORM models (Base, Bronze, Silver)
│   │   ├── base.py
│   │   ├── bronze.py
│   │   └── silver.py
│   ├── pipelines/               # Production ETL execution modules
│   │   ├── runner.py            # Master pipeline orchestrator
│   │   ├── bronze/              # Bronze discovery & extraction (.py)
│   │   ├── silver/              # Silver cleaning & feature engineering (.py)
│   │   └── gold/                # Gold market analysis & arbitrage (.py)
│   ├── scraper/                 # Resilient HTTP scraping engine
│   │   └── engine.py
│   ├── services/                # Marketplace parsing services & crawlers
│   │   ├── olx_service.py
│   │   └── crawlers/
│   │       └── olx_crawler.py
│   └── utils/                   # Shared utility modules
│       ├── get_httpx_client.py
│       └── read_metadata.py
├── notebooks/                   # Interactive Jupyter notebooks for experimentation
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── metadata/                    # Configuration as code (YAML)
│   ├── additional_info.yml
│   ├── scraping_targets.yml
│   └── search_locations.yml
├── docker-compose.yml           # Database infrastructure setup
├── main.py                      # Main entry point script
├── pyproject.toml               # project metadata and dependencies
└── uv.lock                      # Locked dependencies
```
