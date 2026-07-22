# Bronze Pipelines (`app/pipelines/bronze/`)

Executes asynchronous ingestion pipelines for the Bronze layer.

## Pipelines

- **`discover.py` (`run_discover_pipeline`)**: Queries search targets from metadata YAMLs and saves raw discovered listing links to `bronze.GeneralSearch`.
- **`extraction.py` (`run_extraction_pipeline`)**: Scrapes detailed HTML/JSON specifications for discovered links and persists raw attributes to `bronze.InformationExtraction`.

## Related Links
- [Pipelines Overview](../README.md)
- [Bronze Models](../../models/bronze/README.md)
- [Services & Crawlers](../../services/README.md)
