# Marketplace Crawlers (`app/services/crawlers/`)

Implements targeted web scraper crawlers responsible for executing discovery searches and page extraction loops across marketplace websites.

## Components

- **`olx_crawler.py`**: `OLXCrawler` class. Implements async page retrieval, listing discovery link extraction, and detailed page scraping for OLX marketplace categories.

## Execution Dependencies

- **Scraper Engine (`app/scraper/engine.py`)**: Provides async HTTP transport with retry logic, user-agent rotation, and rate-limiting.
- **Parsing Helpers (`app/services/olx_service.py`)**: Utility functions for extracting raw fields, images, prices, and HTML specs.
- **Bronze Models (`app/models/bronze/`)**: `GeneralSearch` and `InformationExtraction` SQLAlchemy models for persisting scraped data.

## Related Links
- [Services Overview](../README.md)
- [OLX Service](../olx_service.py)
- [Scraper Engine](../../scraper/README.md)
- [Bronze Models](../../models/bronze/README.md)
- [Bronze Pipelines](../../pipelines/bronze/README.md)
