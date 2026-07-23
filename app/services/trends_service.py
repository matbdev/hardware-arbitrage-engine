"""
Service layer module for querying Gold layer Market Price Trend analytics.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import FactMarketTrend


def get_market_trends_by_category(
    db: Session,
    category: str
):
    """
    Retrieves macro-level market price trends and volume statistics for a specific category.

    Args:
        db (Session): Active SQLAlchemy database session.
        category (str): Product category classification name (e.g. 'notebook').

    Returns:
        FactMarketTrend | None: Matching market trend record ORM instance or None if not found.
    """
    query = select(FactMarketTrend).where(FactMarketTrend.category == category)
    item = db.execute(query).scalar()
    return item