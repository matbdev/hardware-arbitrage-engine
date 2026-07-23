"""
Gold Layer Product Dimension Model.
Represents unique hardware product configurations (baseline models) for dimensional analysis.
"""
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class DimProduct(Base):
    """
    SQLAlchemy model representing the 'dim_products' table.
    Stores unique hardware product specifications identified by baseline_id.
    """
    __tablename__ = 'dim_products'
    __table_args__ = {"schema": "gold"}

    # Primary key linking unique product baseline configurations
    baseline_id: Mapped[str] = mapped_column(primary_key=True)
    
    # Product classification attributes
    category: Mapped[str]
    brand: Mapped[str]
    cpu_brand: Mapped[str]
    cpu_model: Mapped[str]
    ram_gb: Mapped[int]
    storage_gb: Mapped[int]
    
    # Formatted summary of specifications (e.g., 'i7-10700K, 16GB RAM, 512GB SSD')
    specs_summary: Mapped[str]
