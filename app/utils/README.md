# Utilities (`app/utils/`)

Provides application-wide utility modules and metadata helper functions.

## Components

- **`get_httpx_client.py`**: Configures reusable `httpx.AsyncClient` instances with custom headers and timeout settings.
- **`read_metadata.py`**: Helper functions (`read_search_locations_metadata()`, `read_scraping_targets_metadata()`) for loading YAML configuration files from `metadata/`.

## Related Links
- [Metadata Directory](../../metadata/README.md)
- [Scraper Engine](../scraper/README.md)
