# Silver Pipelines (`app/pipelines/silver/`)

Executes ETL cleaning, normalization, and feature engineering for the Silver layer.

## Pipelines

- **`cleaning.py` (`run_cleaning_pipeline`)**: Reads raw Bronze records, normalizes title casing, extracts numeric specs (RAM, CPU, storage), applies regex flags (`needs_repair`, `urgent_sale`), encodes product characteristics, and saves clean records to `silver.SilverCleanAd`.

## Related Links
- [Pipelines Overview](../README.md)
- [Silver Models](../../models/silver/README.md)
