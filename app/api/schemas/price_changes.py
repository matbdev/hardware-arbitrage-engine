"""
Gold Layer Price Changes Alert Pydantic Schema.
Data Transfer Object (DTO) for serving advertisement price variations, listing age, and discount metrics.
"""
from pydantic import BaseModel, ConfigDict, Field


class PriceChangesAlert(BaseModel):
    """
    Pydantic schema for serializing 'ft_gold_price_changes_alerts' data.
    """
    model_config = ConfigDict(from_attributes=True)

    # Listing identifier primary key
    ad_id: str = Field(..., description="Unique listing identifier", example="olx-987654321")
    
    # Listing details and URL
    title: str = Field(..., description="Listing title", example="Samsung Galaxy Book i5 8GB")
    url: str = Field(..., description="Direct marketplace listing URL", example="https://olx.com.br/vi/987654321")
    
    # Historical price movement metrics
    initial_price: float = Field(..., description="Initial price when first scraped in BRL", example=2000.00)
    current_price: float = Field(..., description="Latest updated price in BRL", example=1600.00)
    
    # Calculated alert indicators
    price_change_pct: float = Field(..., description="Percentage price drop ratio", example=-0.20)
    days_on_market: int = Field(..., description="Number of days listing has been active", example=14)
