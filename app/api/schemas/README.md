# API Schemas (`app/api/schemas/`)

Defines Pydantic V2 Request and Response Data Transfer Objects (DTOs) for serializing database models into JSON API responses with ORM mode (`from_attributes=True`).

## Components

- **`common.py`**: `PaginatedResponse[T]` generic schema envelope (`total`, `page`, `limit`, `total_pages`, `items`).
- **`opportunity.py`**: `ArbitrageOpportunity` schema for serializing high-ROI deal opportunities (`ft_gold_arbitrage_opportunities`).
- **`baseline.py`**: `MarketBaseline` schema for serializing benchmark pricing statistics (`ft_gold_market_baselines`).
- **`price_changes.py`**: `PriceChangesAlert` schema for serializing price reduction alerts (`ft_gold_price_changes_alerts`).
- **`products.py`**: `Product` schema for serializing hardware product dimensions (`dim_products`).
- **`trend.py`**: `MarketTrend` schema for serializing time-series market trend analytics (`ft_gold_market_trends`).

## Usage & Conventions

All schema classes configure `model_config = ConfigDict(from_attributes=True)` to allow direct serialization of SQLAlchemy ORM model instances returned from query services.

```python
from app.api.schemas import ArbitrageOpportunity, PaginatedResponse
```

## Related Links
- [API Overview](../README.md)
- [API V1 Router](../v1/README.md)
- [API V1 Endpoints](../v1/endpoints/README.md)
- [Gold Models](../../models/gold/README.md)
