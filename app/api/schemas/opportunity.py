"""
Gold Layer Arbitrage Opportunity Pydantic Schema.
Data Transfer Object (DTO) for serving high-ROI deal opportunities evaluated against market medians.
"""
from pydantic import BaseModel, ConfigDict, Field


class ArbitrageOpportunity(BaseModel):
    """
    Pydantic schema for serializing 'ft_gold_arbitrage_opportunities' data.
    """
    model_config = ConfigDict(from_attributes=True)
    
    # Listing identifier primary key
    ad_id: str = Field(..., description="Unique listing identifier from marketplace", example="olx-987654321")
    
    # Baseline product dimension reference
    baseline_id: str = Field(..., description="Product baseline configuration identifier", example="lenovo_i7_16gb_512gb")
    
    # Listing display attributes
    title: str = Field(..., description="Listing title displayed on marketplace", example="Lenovo ThinkPad T14 i7 16GB 512GB SSD")
    url: str = Field(..., description="Direct listing URL link", example="https://olx.com.br/vi/123456789")
    first_image_src: str | None = Field(default=None, description="Primary thumbnail image URL", example="https://img.olx.com.br/images/12.jpg")
    item_condition: str = Field(..., description="Condition state of item (e.g. usado, excelente)", example="usado")
    specs_summary: str = Field(..., description="Formatted summary of extracted specifications", example="Intel Core i7, 16GB RAM, 512GB SSD")
    
    # Deal flag and price comparison metrics
    is_urgent_sale: bool = Field(..., description="Urgent sale indicator detected from listing description", example=False)
    current_price: float = Field(..., description="Current listing price in BRL", example=1800.00)
    market_median_price: float = Field(..., description="Benchmark market median price in BRL", example=2600.00)
    
    # Evaluated profit & ranking metrics
    potential_profit: float = Field(..., description="Calculated gross profit margin in BRL", example=800.00)
    profit_margin_pct: float = Field(..., description="Calculated profit margin percentage ratio", example=0.307)
    opportunity_score: float = Field(..., description="Ranked deal opportunity rating score (0 to 10)", example=9.2)
