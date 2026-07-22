# Models Package (`app/models/`)

Defines all SQLAlchemy ORM database models, structured following the Medallion Data Architecture (Bronze -> Silver -> Gold).

## Layered Model Modules

- **`base.py`**: Common declarative base class (`Base`) for all SQLAlchemy models.
- **[`bronze/`](bronze/README.md)**: Raw ingestion schemas (`GeneralSearch`, `InformationExtraction`).
- **[`silver/`](silver/README.md)**: Cleaned and normalized listings schema (`SilverCleanAd`).
- **[`gold/`](gold/README.md)**: Analytical dimensions and fact tables (`DimProduct`, `FactMarketBaseline`, `FactMarketTrend`, `FactPriceDropAlert`, `FactArbitrageOpportunity`).

## Import Conventions

Models can be imported either via top-level layer namespaces or directly:

```python
# Layer namespace import (Recommended):
from app.models import bronze, silver, gold

# Direct class import:
from app.models.gold import DimProduct, FactMarketBaseline
```

## Related Links
- [App Pipelines](../pipelines/README.md)
