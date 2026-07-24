from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router as api_router_v1

app = FastAPI(
    title="Hardware Arbitrage Engine API",
    description="""
    ## 🚀 Production REST API for Hardware Arbitrage & AI Appraisal

    This API exposes endpoints for:
    * 🎯 **Arbitrage Opportunities**: Active high-ROI deals sorted by opportunity score.
    * 📊 **Market Baselines**: Benchmark prices (min, median, max) per hardware spec.
    * 📈 **Market Trends**: Time-series volume and price movement analytics.
    * 📉 **Price Drop Alerts**: Price variations and days-on-market metrics.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # All by now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Includes all routes
app.include_router(api_router_v1, prefix="/api/v1")