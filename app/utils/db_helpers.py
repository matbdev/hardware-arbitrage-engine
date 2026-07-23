"""
Database utility helper module for query execution and aggregate functions.
"""
from typing import Type
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.base import Base


def count_total_records(
    db: Session,
    model: Type[Base],
    where_clause: object | None = None
) -> int:
    """
    Executes an optimized COUNT query on a given SQLAlchemy model table.
    
    Args:
        db (Session): Active SQLAlchemy database session.
        model (Type[Base]): The SQLAlchemy ORM model class to count rows for.
        where_clause (Optional[Any]): Optional SQLAlchemy filter expression (e.g. Model.margin >= 0.15).
        
    Returns:
        int: Total number of matching records in the database table.
    """
    query = select(func.count()).select_from(model)
    if where_clause is not None:
        query = query.where(where_clause)
    return db.scalar(query) or 0
