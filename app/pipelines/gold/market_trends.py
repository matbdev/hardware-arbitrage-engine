"""
Gold Layer Market Trends Pipeline.
Aggregates macro price trends and listing volume by date, category, and brand.
"""
import polars as pl
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.config import db_engine
from app.models import gold, silver


def run_market_trends_pipeline() -> None:
    """
    Executes the Gold layer market trends analysis pipeline.
    """
    print("Running Gold Layer: Market Trends pipeline...")

    with db_engine.connect() as connection:
        df_silver_raw = pl.read_database(
            select(
                silver.SilverCleanAd.date,
                silver.SilverCleanAd.category,
                silver.SilverCleanAd.brand,
                silver.SilverCleanAd.price,
                silver.SilverCleanAd.ad_id
            ),
            connection=connection
        )

    if df_silver_raw.is_empty():
        print("No Silver clean ads data available for market trends.")
        return

    # Group daily listings by date, category, and brand to compute trend metrics
    df_gold_market_trends = (
        df_silver_raw
        .group_by(['date', 'category', 'brand'])
        .agg(
            pl.col('price').median().alias('median_market_price'),
            pl.col('ad_id').count().alias('total_volume_available')
        )
    )

    if not df_gold_market_trends.is_empty():
        with Session(db_engine) as session:
            session.execute(
                insert(gold.FactMarketTrend), df_gold_market_trends.to_dicts()
            )
            session.commit()
            print(f"Successfully calculated and persisted {len(df_gold_market_trends)} market trend records.")
    else:
        print("No trend data found to insert.")


def run() -> None:
    """
    Synchronous entry point for market trends pipeline execution.
    """
    run_market_trends_pipeline()


if __name__ == "__main__":
    run()
