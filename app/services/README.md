# Application Services (`app/services/`)

Contains business logic query services and marketplace-specific crawler/parsing implementations.

## Business & Query Services

- **`opportunity_service.py`**: Queries Gold layer `FactArbitrageOpportunity` records with profit margin filtering and pagination.
- **`baseline_service.py`**: Queries Gold layer `FactMarketBaseline` price benchmark statistics.
- **`price_changes_service.py`**: Queries Gold layer `FactPriceDropAlert` price reduction alerts.
- **`product_service.py`**: Queries Gold layer `DimProduct` normalized hardware product dimensions.
- **`trends_service.py`**: Queries Gold layer `FactMarketTrend` time-series market trend analytics.

## Marketplace Crawlers & Scrapers

- **`olx_service.py`**: Parsing helper functions for extracting product titles, prices, descriptions, images, and HTML specifications from OLX marketplace pages.
- **[`crawlers/`](crawlers/README.md)**: Targeted marketplace crawlers (`OLXCrawler`). Handles general link discovery and detailed page extraction loops for OLX listings.

## Related Links
- [REST API Package](../api/README.md)
- [Crawlers Module](crawlers/README.md)
- [Scraper Engine](../scraper/README.md)
- [Bronze Pipelines](../pipelines/bronze/README.md)
