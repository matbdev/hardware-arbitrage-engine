# Bronze Models (`app/models/bronze/`)

Contains SQLAlchemy ORM models for raw data ingested during the scraping phase.

## Models

- **`general_search.py` (`GeneralSearch`)**: Represents the `bronze_ad_links` table. Stores raw listing URLs discovered during search discovery.
- **`information_extraction.py` (`InformationExtraction`)**: Represents the `bronze_extraction_data` table. Stores raw HTML/JSON extracted listing details (titles, descriptions, raw specs).

## Related Links
- [Models Overview](../README.md)
- [Bronze Pipelines](../../pipelines/bronze/README.md)
