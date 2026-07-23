"""
Service layer module for querying Gold layer Market Price Baselines.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import FactMarketBaseline


def get_baseline_by_id(db: Session, baseline_id: str):
    """
    Retrieves a single Market Baseline benchmark record matching the given baseline_id.

    Args:
        db (Session): Active SQLAlchemy database session.
        baseline_id (str): Unique hardware configuration baseline identifier.

    Returns:
        FactMarketBaseline | None: Matching baseline ORM instance or None if not found.
    """
    query = select(FactMarketBaseline).where(FactMarketBaseline.baseline_id == baseline_id)
    item = db.scalar(query)
    return item