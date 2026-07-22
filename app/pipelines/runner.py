"""
Pipeline orchestrator module.
Provides functions to trigger execution of Bronze, Silver, and Gold data pipelines.
"""
import asyncio

from app.pipelines.bronze.discover import run_discover_pipeline
from app.pipelines.bronze.extraction import run_extraction_pipeline
from app.pipelines.gold.arbitrage_opportunities import (
    run_arbitrage_opportunities_pipeline,
)
from app.pipelines.gold.market_baselines import run_market_baselines_pipeline
from app.pipelines.gold.market_trends import run_market_trends_pipeline
from app.pipelines.gold.price_drop_alerts import run_price_drop_alerts_pipeline
from app.pipelines.silver.cleaning import run_cleaning_pipeline


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
    Executes the Gold layer pipelines (arbitrage opportunities, market baselines, price drop alerts, market trends).
    """
    print("Running Gold Arbitrage Opportunities...")
    run_arbitrage_opportunities_pipeline()

    print("Running Gold Market Baselines...")
    run_market_baselines_pipeline()

    print("Running Gold Price Drop Alerts...")
    run_price_drop_alerts_pipeline()

    print("Running Gold Market Trends...")
    run_market_trends_pipeline()


if __name__ == "__main__":
    run_pipelines()