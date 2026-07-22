# Marketplace Services (`app/services/`)

Contains marketplace-specific crawler implementations and HTML/JSON parsing services.

## Submodules

- **`olx_service.py`**: Parsing helper functions for extracting product titles, prices, descriptions, images, and HTML specifications from OLX marketplace pages.
- **`crawlers/olx_crawler.py`**: `OLXCrawler` class. Handles general link search discovery and detailed listing extraction loops for OLX listings.

## Related Links
- [Scraper Engine](../scraper/README.md)
- [Bronze Pipelines](../pipelines/bronze/README.md)
