"""
Gold Layer Price Drop Alert Fact Model.
Tracks advertisement price variations, listing age, and percentage drops over time.
"""
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class FactPriceDropAlert(Base):
    """
    SQLAlchemy model representing the 'ft_gold_price_drop_alerts' table.
    Stores alerts for listing price drops and market duration tracking.
    """
    __tablename__ = 'ft_gold_price_drop_alerts'

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
