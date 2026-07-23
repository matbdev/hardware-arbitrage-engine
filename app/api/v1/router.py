from fastapi import APIRouter

from app.api.v1.endpoints import (
    baselines_router,
    health_router,
    opportunities_router,
    price_changes_router,
    products_router,
    trends_router,
)

api_router = APIRouter()

# Register all v1 API route modules
api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(opportunities_router, prefix="/opportunities", tags=["Opportunities"])
api_router.include_router(baselines_router, prefix="/baselines", tags=["Baselines"])
api_router.include_router(price_changes_router, prefix="/price-changes", tags=["Price Changes"])
api_router.include_router(products_router, prefix="/products", tags=["Products"])
api_router.include_router(trends_router, prefix="/trends", tags=["Trends"])