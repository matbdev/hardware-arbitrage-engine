# Gold Models (`app/models/gold/`)

Contains SQLAlchemy ORM models for analytical dimensions and fact tables in the Gold layer.

## Models

- **`dim_product.py` (`DimProduct`)**: `dim_products` table. Stores unique product baseline hardware configurations and formatted specification summaries (`specs_summary`).
- **`fact_market_baseline.py` (`FactMarketBaseline`)**: `ft_gold_market_baselines` table. Stores pricing benchmarks (minimum, median, maximum) per baseline model.
- **`fact_market_trend.py` (`FactMarketTrend`)**: `ft_gold_market_trends` table. Stores daily macro price trends and listing volume by category and brand.
- **`fact_price_drop_alert.py` (`FactPriceDropAlert`)**: `ft_gold_price_drop_alerts` table. Stores price drop alerts and days active on market.
- **`fact_arbitrage_opportunity.py` (`FactArbitrageOpportunity`)**: `ft_gold_arbitrage_opportunities` table. Stores high-ROI deal opportunities evaluated against market medians.

## Related Links
- [Models Overview](../README.md)
- [Gold Pipelines](../../pipelines/gold/README.md)
