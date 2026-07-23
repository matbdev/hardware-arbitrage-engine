from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas import PaginatedResponse, PriceChangesAlert
from app.services import price_changes_service

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[PriceChangesAlert],
    status_code=status.HTTP_200_OK,
    summary="List Price Change Alerts",
    description="Retrieves a paginated list of listing price variations, discount percentages, and days-on-market metrics."
)
def get_price_changes(
    page: int = Query(default=1, ge=1, description="Page number for pagination"),
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of items per page"),
    db: Session = Depends(get_db)
):
    try:
        return price_changes_service.get_changes(
            db,
            limit=limit,
            page=page
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database connection failed: {str(e)}"
        )