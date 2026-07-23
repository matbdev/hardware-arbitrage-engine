from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db

router = APIRouter()


@router.get(
    "/live",
    status_code=status.HTTP_200_OK,
    summary="Application Liveness Check",
    description="Returns HTTP 200 if the web server is online and serving requests."
)
async def liveness_check():
    """Checks if the server is on"""
    return {"status": "alive"}


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    summary="Database Readiness Check",
    description="Executes a SELECT 1 query to verify active connectivity with the PostgreSQL database."
)
async def readiness_check(db: Session = Depends(get_db)):
    """Checks if the database is on"""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )