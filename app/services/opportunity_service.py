"""
Service layer module for querying and paginating Gold layer Arbitrage Opportunities.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import FactArbitrageOpportunity
from app.utils import (
    build_paginated_response,
    calculate_offset,
    count_total_records,
)


def get_top_deals(
    db: Session,
    min_margin: float,
    limit: int,
    page: int
):
    """
    Fetches a paginated list of high-ROI arbitrage deals filtered by minimum profit margin ratio.

    Args:
        db (Session): Active SQLAlchemy database session.
        min_margin (float): Minimum profit margin percentage threshold (e.g. 0.10 for 10%).
        limit (int): Number of items to return per page.
        page (int): Page number (1-indexed).

    Returns:
        dict: Standardized paginated envelope dictionary with total metadata and items list.
    """
    # Calculates SQL query offset
    offset = calculate_offset(page=page, limit=limit)

    # Filter expression for minimum profit margin
    where_clause = FactArbitrageOpportunity.profit_margin_pct >= min_margin

    # Calculates the total number of matching records in database
    total_records = count_total_records(
        db=db,
        model=FactArbitrageOpportunity,
        where_clause=where_clause
    )

    # Gets the paginated records sorted by opportunity score
    query = (
        select(FactArbitrageOpportunity)
        .where(where_clause)
        .order_by(FactArbitrageOpportunity.opportunity_score.desc())
        .offset(offset)
        .limit(limit)
    )
    items = db.execute(query).scalars().all()

    # Builds the JSON response envelope and returns it
    return build_paginated_response(
        items=items,
        limit=limit,
        total_items=total_records,
        page=page
    )