"""
Gold Layer Price Changes Alert Fact Model.
Tracks advertisement price variations, listing age, and percentage changes over time.
"""
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class FactPriceChangesAlert(Base):
    """
    SQLAlchemy model representing the 'ft_gold_price_changes_alerts' table.
    Stores alerts for listing price changes and market duration tracking.
    """
    __tablename__ = 'ft_gold_price_changes_alerts'
    __table_args__ = {"schema": "gold"}

    # Listing identifier primary key
    ad_id: Mapped[str] = mapped_column(primary_key=True)
    
    # Listing details and URL
    title: Mapped[str]
    url: Mapped[str]
    
    # Historical price movement metrics
    initial_price: Mapped[float]
    current_price: Mapped[float]
    
    # Calculated alert indicators
    price_change_pct: Mapped[float]
    days_on_market: Mapped[int]
