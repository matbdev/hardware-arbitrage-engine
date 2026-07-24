from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    """Standard envelope for paginated list endpoints."""
    total: int
    page: int
    limit: int
    total_pages: int
    items: List[T]