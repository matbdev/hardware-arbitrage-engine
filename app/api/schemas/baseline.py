"""
Gold Layer Market Baseline Pydantic Schema.
Data Transfer Object (DTO) for serving aggregated price benchmarks (min, median, max) per hardware configuration.
"""
from datetime import date as DateType
from pydantic import BaseModel, ConfigDict, Field


class MarketBaseline(BaseModel):
    """
    Pydantic schema for serializing 'ft_gold_market_baselines' benchmark data.
    """
    model_config = ConfigDict(from_attributes=True)

    # Auto-incrementing primary key
    id: int = Field(..., description="Internal auto-incrementing database primary key ID", example=1)
    
    # Unique product baseline reference identifier
    baseline_id: str = Field(..., description="Unique product configuration identifier", example="lenovo_i7_16gb_512gb")
    
    # Product dimension attributes
    category: str = Field(..., description="Product hardware category classification", example="notebook")
    cpu_brand: str = Field(..., description="CPU processor brand name", example="Intel")
    ram_gb: int = Field(..., description="System RAM memory size in gigabytes", example=16)
    storage_gb: int = Field(..., description="System storage capacity in gigabytes", example=512)
    
    # Aggregated price and volume metrics
    active_ads_count: int = Field(..., description="Total count of active marketplace listings used for baseline calculation", example=42)
    min_price: float = Field(..., description="Minimum listing price observed in market sample in BRL", example=1500.00)
    median_price: float = Field(..., description="Median benchmark market price in BRL", example=2600.00)
    max_price: float = Field(..., description="Maximum listing price observed in market sample in BRL", example=3500.00)
    
    # Recalculation timestamp tracking
    last_recalculated_at: DateType = Field(..., description="Date of last baseline recalculation snapshot", example="2026-07-23")
