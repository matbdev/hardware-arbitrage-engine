"""
Service layer module for querying and paginating Gold layer Price Changes Alerts.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import FactPriceDropAlert
from app.utils import (
    build_paginated_response,
    calculate_offset,
    count_total_records,
)


def get_changes(
    db: Session,
    limit: int,
    page: int
):
    """
    Fetches a paginated list of listing price reduction alerts and market age metrics.

    Args:
        db (Session): Active SQLAlchemy database session.
        limit (int): Number of items to return per page.
        page (int): Page number (1-indexed).

    Returns:
        dict: Standardized paginated envelope dictionary with metadata and items.
    """
    # Calculates SQL query offset
    offset = calculate_offset(page=page, limit=limit)

    # Calculates the total number of alert records
    total_records = count_total_records(
        db=db,
        model=FactPriceDropAlert
    )

    # Gets the paginated records
    query = (
        select(FactPriceDropAlert)
        .offset(offset)
        .limit(limit)
    )
    items = db.execute(query).scalars().all()

    # Builds the JSON envelope and returns it
    return build_paginated_response(
        items=items,
        limit=limit,
        total_items=total_records,
        page=page
    )