"""
Pagination utility module for database queries and API response envelope formatting.
"""
import math


def calculate_offset(page: int, limit: int) -> int:
    """
    Calculates SQL database query offset based on page number and limit size.
    Ensures offset is non-negative even if page index is less than 1.
    """
    return max(0, (page - 1) * limit)


def calculate_total_pages(total_items: int, limit: int) -> int:
    """
    Calculates the total number of pages based on total records count and page limit size.
    """
    if limit <= 0:
        return 1
    return math.ceil(total_items / limit) if total_items > 0 else 1


def build_paginated_response[T](
    items: list[T],
    total_items: int,
    page: int,
    limit: int
) -> dict[str, object]:
    """
    Builds a standardized paginated response dictionary containing metadata and items list.
    """
    return {
        "total": total_items,
        "page": page,
        "limit": limit,
        "total_pages": calculate_total_pages(total_items, limit),
        "items": items,
    }
