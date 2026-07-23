from .baselines import router as baselines_router
from .health import router as health_router
from .opportunities import router as opportunities_router
from .price_changes import router as price_changes_router
from .products import router as products_router
from .trends import router as trends_router

__all__ = [
    "baselines_router",
    "health_router",
    "opportunities_router",
    "price_changes_router",
    "products_router",
    "trends_router",
]