"""
Database models package export.
Organized into bronze, silver, and gold layer modules.
"""
from .base import Base
from . import bronze
from . import silver
from . import gold

# Direct class exports for backward compatibility and top-level convenience
from .bronze import GeneralSearch, InformationExtraction
from .silver import SilverCleanAd
from .gold import (
    DimProduct,
    FactMarketBaseline,
    FactMarketTrend,
    FactPriceDropAlert,
    FactArbitrageOpportunity,
)

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