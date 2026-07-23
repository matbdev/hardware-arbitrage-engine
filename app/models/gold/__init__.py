from .dim_product import DimProduct
from .fact_arbitrage_opportunity import FactArbitrageOpportunity
from .fact_market_baseline import FactMarketBaseline
from .fact_market_trend import FactMarketTrend
from .ft_price_changes_alert import FactPriceChangesAlert

FactPriceDropAlert = FactPriceChangesAlert

__all__ = [
    "DimProduct",
    "FactMarketBaseline",
    "FactMarketTrend",
    "FactPriceChangesAlert",
    "FactPriceDropAlert",
    "FactArbitrageOpportunity",
]
