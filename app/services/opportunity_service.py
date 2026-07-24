"""
Service layer module for querying and paginating Gold layer Arbitrage Opportunities.
"""
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models import FactArbitrageOpportunity
from app.utils import (
    build_paginated_response,
    calculate_offset,
    count_total_records,
)


def get_top_deals(
    db: Session,
    min_margin: float | None = 0.10,
    max_price: float | None = None,
    limit: int = 50,
    page: int = 1
):
    """
    Fetches a paginated list of high-ROI arbitrage deals filtered by minimum profit margin ratio and/or maximum price.

    Args:
        db (Session): Active SQLAlchemy database session.
        min_margin (float | None): Optional minimum profit margin percentage threshold (e.g. 0.10 for 10%).
        max_price (float | None): Optional maximum listing current price in BRL.
        limit (int): Number of items to return per page.
        page (int): Page number (1-indexed).

    Returns:
        dict: Standardized paginated envelope dictionary with total metadata and items list.
    """
    # Build dynamic filter expressions
    conditions = []
    if min_margin is not None:
        conditions.append(FactArbitrageOpportunity.profit_margin_pct >= min_margin)
    if max_price is not None:
        conditions.append(FactArbitrageOpportunity.current_price <= max_price)

    where_clause = and_(*conditions) if conditions else None

    # Calculates SQL query offset
    offset = calculate_offset(page=page, limit=limit)

    # Calculates total number of matching records in database
    total_records = count_total_records(
        db=db,
        model=FactArbitrageOpportunity,
        where_clause=where_clause
    )

    # Builds query for matching records sorted by opportunity score
    query = select(FactArbitrageOpportunity)
    if where_clause is not None:
        query = query.where(where_clause)

    query = query.order_by(FactArbitrageOpportunity.opportunity_score.desc()).offset(offset).limit(limit)
    items = db.execute(query).scalars().all()

    # Builds JSON response envelope and returns it
    return build_paginated_response(
        items=items,
        limit=limit,
        total_items=total_records,
        page=page
    )