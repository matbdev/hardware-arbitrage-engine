# Utilities (`app/utils/`)

Provides application-wide utility modules, pagination helpers, database count functions, and metadata helper functions.

## Components

- **`pagination.py`**: Utilities for calculating SQL query offsets (`calculate_offset`), total pages (`calculate_total_pages`), and building paginated response envelopes (`build_paginated_response`).
- **`db_helpers.py`**: Optimized database aggregate query helper (`count_total_records`) for counting rows in SQLAlchemy tables.
- **`get_httpx_client.py`**: Configures reusable `httpx.AsyncClient` instances with custom headers and timeout settings.
- **`read_metadata.py`**: Helper functions (`read_search_locations_metadata()`, `read_scraping_targets_metadata()`) for loading YAML configuration files from `metadata/`.

## Related Links
- [REST API Package](../api/README.md)
- [Metadata Directory](../../metadata/README.md)
- [Scraper Engine](../scraper/README.md)
