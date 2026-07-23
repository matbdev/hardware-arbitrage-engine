"""
Service layer module for querying and paginating Gold layer Product Dimensions.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import DimProduct
from app.utils import (
    build_paginated_response,
    calculate_offset,
    count_total_records,
)


def get_products_by_baseline_id(
    db: Session,
    baseline_id: str,
    limit: int,
    page: int
):
    """
    Fetches a paginated list of normalized hardware product dimensions filtered optionally by baseline_id.

    Args:
        db (Session): Active SQLAlchemy database session.
        baseline_id (str): Optional baseline identifier filter.
        limit (int): Number of items per page.
        page (int): Page number (1-indexed).

    Returns:
        dict: Standardized paginated envelope dictionary.
    """
    # Calculates SQL query offset
    offset = calculate_offset(page=page, limit=limit)

    # Optional filter expression
    where_clause = DimProduct.baseline_id == baseline_id if baseline_id else None

    # Calculates the total number of records
    total_records = count_total_records(
        db=db,
        model=DimProduct,
        where_clause=where_clause
    )

    # Gets the paginated records
    query = select(DimProduct)
    if where_clause is not None:
        query = query.where(where_clause)
        
    query = query.offset(offset).limit(limit)
    items = db.execute(query).scalars().all()

    # Builds the JSON response envelope and returns it
    return build_paginated_response(
        items=items,
        limit=limit,
        total_items=total_records,
        page=page
    )