"""
Gold Layer Market Trend Fact Model.
Tracks macro-level price trends and listing volume over time by date, category, and brand.
"""
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class FactMarketTrend(Base):
    """
    SQLAlchemy model representing the 'ft_gold_market_trends' table.
    Stores daily aggregated price trends and listing volumes by hardware category and brand.
    """
    __tablename__ = 'ft_gold_market_trends'

    # Auto-incrementing primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Snapshot date for time series tracking
    date: Mapped[date]
    
    # Product grouping dimensions
    category: Mapped[str]
    brand: Mapped[str]
    
    # Macro market metrics
    median_market_price: Mapped[float]
    total_volume_available: Mapped[int]
