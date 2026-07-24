"""
Database models package export.
Organized into bronze, silver, and gold layer modules.
"""
from . import bronze, gold, silver
from .base import Base

# Direct class exports for backward compatibility and top-level convenience
from .bronze import GeneralSearch, InformationExtraction
from .gold import (
    DimProduct,
    FactArbitrageOpportunity,
    FactMarketBaseline,
    FactMarketTrend,
    FactPriceDropAlert,
)
from .silver import SilverCleanAd

__all__ = [
    "Base",
    "bronze",
    "silver",
    "gold",
    "GeneralSearch",
    "InformationExtraction",
    "SilverCleanAd",
    "DimProduct",
    "FactMarketBaseline",
    "FactMarketTrend",
    "FactPriceDropAlert",
    "FactArbitrageOpportunity",
]