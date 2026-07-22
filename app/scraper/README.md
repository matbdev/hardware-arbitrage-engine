# Scraper Engine (`app/scraper/`)

Provides resilient asynchronous HTTP scraping utilities for web scraping operations.

## Components

- **`engine.py`**: Contains `scrape_url()`, built with `httpx` async calls, automatic Exponential Backoff retries via Tenacity, custom User-Agent rotation, and 403/429 anti-bot handling.

## Related Links
- [App Overview](../README.md)
- [Marketplace Services](../services/README.md)
