from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas import ArbitrageOpportunity, PaginatedResponse
from app.services import opportunity_service

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[ArbitrageOpportunity],
    status_code=status.HTTP_200_OK,
    summary="List Top Arbitrage Deal Opportunities",
    description="Retrieves a paginated list of high-ROI hardware deal opportunities filtered by profit margin and/or maximum price, sorted by opportunity score."
)
def list_opportunities(
    min_margin: float | None = Query(default=0.10, ge=0.0, le=1.0, description="Optional minimum profit margin percentage (e.g. 0.15 for 15%)"),
    max_price: float | None = Query(default=None, gt=0.0, description="Optional maximum listing price in BRL (e.g. 2000.0)"),
    page: int = Query(default=1, ge=1, description="Page number for pagination"),
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of items per page"),
    db: Session = Depends(get_db)
):
    try:
        return opportunity_service.get_top_deals(
            db,
            min_margin=min_margin,
            max_price=max_price,
            limit=limit,
            page=page
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database connection failed: {str(e)}"
        )