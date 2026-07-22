"""
Pipeline orchestrator module.
Provides functions to trigger execution of Bronze, Silver, and Gold data pipelines.
"""
import asyncio

from app.pipelines.bronze.discover import run_discover_pipeline
from app.pipelines.bronze.extraction import run_extraction_pipeline
from app.pipelines.silver.cleaning import run_cleaning_pipeline

# Gold pipelines ordered strictly by data dependency:
from app.pipelines.gold.dim_products import run_dim_products_pipeline
from app.pipelines.gold.market_baselines import run_market_baselines_pipeline
from app.pipelines.gold.market_trends import run_market_trends_pipeline
from app.pipelines.gold.price_drop_alerts import run_price_drop_alerts_pipeline
from app.pipelines.gold.arbitrage_opportunities import (
    run_arbitrage_opportunities_pipeline,
)


def run_pipelines() -> None:
    """
    Executes the full data pipeline across Bronze, Silver, and Gold layers sequentially.
    """
    print("Starting Bronze layer execution...")
    run_bronze_pipeline()

    print("Starting Silver layer execution...")
    run_silver_pipeline()

    print("Starting Gold layer execution...")
    run_gold_pipeline()


def run_bronze_pipeline() -> None:
    """
    Executes the Bronze layer pipelines (discover and extraction).
    """
    print("Running Bronze Discovery...")
    asyncio.run(run_discover_pipeline())

    print("Running Bronze Extraction...")
    asyncio.run(run_extraction_pipeline())


def run_silver_pipeline() -> None:
    """
    Executes the Silver layer pipeline (cleaning & feature engineering).
    """
    print("Running Silver Cleaning...")
    run_cleaning_pipeline()


def run_gold_pipeline() -> None:
    """
    Executes Gold layer pipelines in strict dependency order:
    1. Product Dimensions (dim_products)
    2. Market Baselines (ft_gold_market_baselines)
    3. Market Trends (ft_gold_market_trends)
    4. Price Drop Alerts (ft_gold_price_drop_alerts)
    5. Arbitrage Opportunities (ft_gold_arbitrage_opportunities - requires dim_products & market_baselines)
    """
    print("1. Running Gold Product Dimensions...")
    run_dim_products_pipeline()

    print("2. Running Gold Market Baselines...")
    run_market_baselines_pipeline()

    print("3. Running Gold Market Trends...")
    run_market_trends_pipeline()

    print("4. Running Gold Price Drop Alerts...")
    run_price_drop_alerts_pipeline()

    print("5. Running Gold Arbitrage Opportunities...")
    run_arbitrage_opportunities_pipeline()


if __name__ == "__main__":
    run_pipelines()