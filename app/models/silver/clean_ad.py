from datetime import date
from typing import Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class SilverCleanAd(Base):
    """
    SQLAlchemy model representing the 'silver_clean_ads' table.
    Stores the cleaned, normalized, and feature-engineered advertisement data.
    """
    __tablename__ = "silver_clean_ads"
    __table_args__ = {"schema": "silver"}

    id: Mapped[int] = mapped_column(primary_key=True)
    ad_id: Mapped[str]
    date: Mapped[date]
    category: Mapped[str]
    subcategory: Mapped[str]
    item: Mapped[str]
    brand: Mapped[str]
    item_condition: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    currency: Mapped[str]
    ram_gb: Mapped[Optional[float]]
    storage_gb: Mapped[Optional[float]]
    cpu_brand: Mapped[str]
    cpu_model: Mapped[str]
    gpu_brand: Mapped[str]
    screen_size_pol: Mapped[Optional[float]]
    for_donation: Mapped[bool]
    accept_trades: Mapped[bool]
    region: Mapped[str]
    store: Mapped[str]
    url: Mapped[str]
    link: Mapped[str]
    first_image_src: Mapped[str]
    characteristics: Mapped[list[str]] = mapped_column(JSON)
    baseline_id: Mapped[str]
    
    # Feature Engineering Flags
    needs_repair: Mapped[bool]
    urgent_sale: Mapped[bool]
    item_condition_indicator: Mapped[int]
    
    # One-Hot Encoding of characteristics
    has_accessories: Mapped[bool]
    has_bluetooth: Mapped[bool]
    has_cables: Mapped[bool]
    has_hdmi: Mapped[bool]
    has_ssd: Mapped[bool]
    has_wifi: Mapped[bool]
