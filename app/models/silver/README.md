# Silver Models (`app/models/silver/`)

Contains SQLAlchemy ORM models for cleaned, normalized, and feature-engineered advertisement data.

## Models

- **`clean_ad.py` (`SilverCleanAd`)**: Represents the `silver_clean_ads` table. Stores normalized titles, extracted specs (RAM, CPU, storage, screen size), regex defect/urgency flags, and one-hot encoded characteristics.

## Related Links
- [Models Overview](../README.md)
- [Silver Pipelines](../../pipelines/silver/README.md)
