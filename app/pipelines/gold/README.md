# Gold Pipelines (`app/pipelines/gold/`)

Executes Gold layer analytical pipelines in strict data dependency order.

## Execution Order

1. **`dim_products.py` (`run_dim_products_pipeline`)**: Populates `gold.DimProduct` with unique baseline product configurations and `specs_summary`.
2. **`market_baselines.py` (`run_market_baselines_pipeline`)**: Computes benchmark pricing statistics (min, median, max) per baseline and saves to `gold.FactMarketBaseline`.
3. **`market_trends.py` (`run_market_trends_pipeline`)**: Aggregates macro price trends and listing volume by category and brand into `gold.FactMarketTrend`.
4. **`price_drop_alerts.py` (`run_price_drop_alerts_pipeline`)**: Tracks price drop variations over time into `gold.FactPriceDropAlert`.
5. **`arbitrage_opportunities.py` (`run_arbitrage_opportunities_pipeline`)**: Joins clean ads with `gold.DimProduct` (for `specs_summary`) and `gold.FactMarketBaseline` (for median price), computes potential profit, margin %, and opportunity scores, and saves to `gold.FactArbitrageOpportunity`.

## Related Links
- [Pipelines Overview](../README.md)
- [Gold Models](../../models/gold/README.md)
