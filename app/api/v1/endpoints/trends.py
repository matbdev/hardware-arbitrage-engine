from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas import MarketTrend
from app.services import trends_service

router = APIRouter()


@router.get(
    "/",
    response_model=MarketTrend,
    status_code=status.HTTP_200_OK,
    summary="Get Market Price Trend Analytics",
    description="Retrieves macro-level price trends and listing volume stats for a specific product category."
)
def get_market_trends_by_category(
    category: str = Query(default="", description="Product category filter (e.g. notebook)"),
    db: Session = Depends(get_db)
):
    try:
        market_trends = trends_service.get_market_trends_by_category(
            db,
            category=category
        )

        if market_trends is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No trend record found for category '{category}'."
            )
        return market_trends
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database connection failed: {str(e)}"
        )