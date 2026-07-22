from .base import Base
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column

class GoldMarketTrend(Base):
    __tablename__ = 'ft_gold_market_trends'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[date]
    category: Mapped[str]
    brand: Mapped[str]
    median_market_price: Mapped[float]
    total_volume_available: Mapped[int]


class GoldMarketBaseline(Base):
    __tablename__ = 'ft_gold_market_baselines'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    baseline_id: Mapped[str] = mapped_column(unique=True)
    
    # Dimension attributes
    category: Mapped[str]
    cpu_brand: Mapped[str]
    ram_gb: Mapped[int]
    storage_gb: Mapped[int]
    
    # Calculated metrics
    active_ads_count: Mapped[int]
    min_price: Mapped[float]
    median_price: Mapped[float]
    max_price: Mapped[float]
    
    # Time control
    last_recalculated_at: Mapped[date]


class GoldPriceVariationAlert(Base):
    __tablename__ = 'ft_gold_price_drop_alerts'

    ad_id: Mapped[str] = mapped_column(primary_key=True)
    
    title: Mapped[str]
    url: Mapped[str]
    
    initial_price: Mapped[float]
    current_price: Mapped[float]
    
    price_change_pct: Mapped[float]
    days_on_market: Mapped[int]


class DimProduct(Base):
    __tablename__ = 'dim_products'

    baseline_id: Mapped[str] = mapped_column(primary_key=True)
    
    category: Mapped[str]
    brand: Mapped[str]
    cpu_brand: Mapped[str]
    cpu_model: Mapped[str]
    ram_gb: Mapped[int]
    storage_gb: Mapped[int]
    specs_summary: Mapped[str]