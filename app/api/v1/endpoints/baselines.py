from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas import MarketBaseline
from app.services import baseline_service

router = APIRouter()


@router.get(
    "/",
    response_model=MarketBaseline,
    status_code=status.HTTP_200_OK,
    summary="Get Market Price Baseline Details",
    description="Retrieves benchmark pricing statistics (min, median, max) for a specific hardware baseline configuration."
)
def get_baselines(
    baseline_id: str = Query(default="", description="Unique product baseline identifier"),
    db: Session = Depends(get_db)
):
    try:
        item = baseline_service.get_baseline_by_id(
            db,
            baseline_id=baseline_id,
        )

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No baseline record found for id '{baseline_id}'."
            )
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database connection failed: {str(e)}"
        )