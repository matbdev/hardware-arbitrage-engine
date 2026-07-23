"""
Gold Layer Market Trend Fact Pydantic Schema.
Data Transfer Object (DTO) for serving time-series market price trends and listing volume analytics.
"""
from datetime import date as DateType
from pydantic import BaseModel, ConfigDict, Field


class MarketTrend(BaseModel):
    """
    Pydantic schema for serializing 'ft_gold_market_trends' time-series data.
    """
    model_config = ConfigDict(from_attributes=True)

    # Auto-incrementing primary key
    id: int = Field(..., description="Internal auto-incrementing primary key ID", example=1)
    
    # Snapshot date for time series tracking
    date: DateType = Field(..., description="Snapshot date of market trend record", example="2026-07-23")
    
    # Product grouping dimensions
    category: str = Field(..., description="Hardware category classification", example="notebook")
    brand: str = Field(..., description="Brand manufacturer name", example="Lenovo")
    
    # Macro market metrics
    median_market_price: float = Field(..., description="Macro median price in BRL for category/brand on snapshot date", example=2600.00)
    total_volume_available: int = Field(..., description="Total active volume count of listings on snapshot date", example=128)
