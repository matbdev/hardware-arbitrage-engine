from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas import PaginatedResponse, Product
from app.services import product_service

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[Product],
    status_code=status.HTTP_200_OK,
    summary="List Hardware Product Configurations",
    description="Retrieves a paginated list of normalized hardware product dimensions and specification summaries."
)
def get_products_by_baseline_id(
    baseline_id: str = Query(default="", description="Optional filter by baseline product configuration ID"),
    page: int = Query(default=1, ge=1, description="Page number for pagination"),
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of items per page"),
    db: Session = Depends(get_db)
):
    try:
        return product_service.get_products_by_baseline_id(
            db,
            baseline_id=baseline_id,
            limit=limit,
            page=page
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database connection failed: {str(e)}"
        )