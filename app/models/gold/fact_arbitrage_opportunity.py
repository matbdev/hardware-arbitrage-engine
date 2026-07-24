"""
Gold Layer Arbitrage Opportunity Fact Model.
Stores detected deals priced significantly below market baseline with calculated ROI and opportunity scores.
"""
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class FactArbitrageOpportunity(Base):
    """
    SQLAlchemy model representing the 'ft_gold_arbitrage_opportunities' table.
    Stores high-value deal opportunities identified by comparing listing prices to market medians.
    """
    __tablename__ = 'ft_gold_arbitrage_opportunities'
    __table_args__ = {"schema": "gold"}

    # Listing identifier primary key
    ad_id: Mapped[str] = mapped_column(primary_key=True)
    
    # Baseline product dimension reference
    baseline_id: Mapped[str]
    
    # Listing display attributes
    title: Mapped[str]
    url: Mapped[str]
    first_image_src: Mapped[Optional[str]]
    item_condition: Mapped[str]
    specs_summary: Mapped[str]
    
    # Deal flag and price comparison metrics
    is_urgent_sale: Mapped[bool]
    current_price: Mapped[float]
    market_median_price: Mapped[float]
    
    # Evaluated profit & ranking metrics
    potential_profit: Mapped[float]
    profit_margin_pct: Mapped[float]
    opportunity_score: Mapped[float]
