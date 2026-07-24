"""
Gold Layer Market Baseline Fact Model.
Stores aggregated market baseline price benchmarks (min, median, max) per hardware product.
"""
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class FactMarketBaseline(Base):
    """
    SQLAlchemy model representing the 'ft_gold_market_baselines' table.
    Stores benchmark price statistics computed per unique product baseline configuration.
    """
    __tablename__ = 'ft_gold_market_baselines'
    __table_args__ = {"schema": "gold"}

    # Auto-incrementing primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Unique product baseline reference identifier
    baseline_id: Mapped[str] = mapped_column(unique=True)
    
    # Product dimension attributes
    category: Mapped[str]
    cpu_brand: Mapped[str]
    ram_gb: Mapped[int]
    storage_gb: Mapped[int]
    
    # Aggregated price and volume metrics
    active_ads_count: Mapped[int]
    min_price: Mapped[float]
    median_price: Mapped[float]
    max_price: Mapped[float]
    
    # Recalculation timestamp tracking
    last_recalculated_at: Mapped[date]
