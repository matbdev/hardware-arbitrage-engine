# Hardware Arbitrage Engine

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-2.13.4-e91e63.svg)
![Polars](https://img.shields.io/badge/Polars-1.40.1-f7a80b.svg)

## Project Overview
An asynchronous web scraping and AI evaluation pipeline designed to identify undervalued used electronics (e.g., Lenovo notebooks, Samsung Galaxy Books) in local classifieds and marketplaces. It combines a Medallion data architecture with an LLM-powered appraisal engine.

## Core Tech Stack
* **Package Management:** uv
* **Backend & API:** httpx
* **Data Validation:** Pydantic (Strict schema enforcement for AI outputs)
* **Data Engineering / Processing:** Polars (Raw to Intermediate to Processed data transformation)
* **AI Integration:** DeepSeek V3 (via OpenRouter API)
* **Storage/State:** PostgreSQL (for final state/dashboard), local Parquet/JSON files (for Data Lake)
* **Scraping:** BeautifulSoup4 / Playwright
* **Configuration:** YAML for search locations and scraping targets
* **Code Quality:** Ruff

## System Architecture
1. **The Scraper (Ingestion / 1.raw):** 
   * `httpx` to fetch live listings asynchronously.
   * Target metadata and search locations are loaded dynamically from `metadata/` YAML files.
   * Raw HTML/JSON dumps are saved locally to the `data/1.raw/` directory.
2. **The Processing Pipeline (2.intermediate):** 
   * `Polars` scripts read the Raw data.
   * Clean text, extract the raw price, normalize specifications (RAM, CPU, condition), and save it as Parquet in `data/2.intermediate/`.
3. **The AI Appraiser (3.processed):** 
   * The pipeline picks up the Intermediate data and formats it into a strict prompt.
   * Sends the structured prompt to DeepSeek V3 via OpenRouter.
   * DeepSeek evaluates the cost-benefit ratio and returns a structured JSON appraisal.
   * Results are stored in `data/3.processed/`.
4. **Serving:**
   * Profitable arbitrage opportunities are pushed to a PostgreSQL database to be served via an API endpoint or dashboard.

## Folder Structure

```text
hardware-arbitrage-engine/
├── app/                         # Application logic
│   ├── core/
│   │   └── config.py            # API keys, DB URIs
│   ├── main.py                  # Project entry point
│   ├── models/
│   │   └── schemas.py           # Pydantic models for listings and AI outputs
│   ├── scrapper/
│   │   └── engine.py            # Async scraping logic
│   └── utils/
│       └── read_metadata.py     # YAML config parser
├── data-processing/             # Data transformation scripts
│   ├── data-engineering/        # Polars ETL scripts (Raw -> Intermediate)
│   └── data-science/            # AI appraiser and modeling logic
├── data/                        # Local data lake
│   ├── 1.raw/                   # Raw JSON/HTML dumps
│   ├── 2.intermediate/          # Cleaned Parquet files
│   └── 3.processed/             # Appraised deals ready for the dashboard
├── metadata/                    # Configuration as code
│   ├── additional_info.yml
│   ├── scraping_targets.yml
│   └── search_locations.yml
├── docker-compose.yml           # PostgreSQL for final state
├── pyproject.toml               # uv project configuration and Ruff settings
├── run.py                       # Project execution entrypoint
└── uv.lock                      # Locked dependencies
```
