"""
Gold Layer Market Baselines Pipeline.
Calculates baseline pricing statistics (min, median, max) per hardware baseline_id.
"""
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
import polars as pl

from app.config import db_engine
from app.models import silver, gold


def run_market_baselines_pipeline() -> None:
    """
    Executes the Gold layer market baseline calculation pipeline.
    """
    print("Running Gold Layer: Market Baselines pipeline...")

    with db_engine.connect() as connection:
        df_silver_raw = pl.read_database(
            select(
                silver.SilverCleanAd.category,
                silver.SilverCleanAd.cpu_brand,
                silver.SilverCleanAd.ram_gb,
                silver.SilverCleanAd.storage_gb,
                silver.SilverCleanAd.ad_id,
                silver.SilverCleanAd.price,
                silver.SilverCleanAd.date,
                silver.SilverCleanAd.baseline_id
            ),
            connection=connection
        )

    if df_silver_raw.is_empty():
        print("No Silver clean ads data available for market baselines.")
        return

    # Compute baseline pricing metrics for the latest listing date per baseline configuration
    market_baselines_df = (
        df_silver_raw
        .filter(
            pl.col('date') == pl.col('date').max().over('baseline_id')
        )
        .group_by(['baseline_id', 'category', 'cpu_brand', 'ram_gb', 'storage_gb'])
        .agg(
            pl.col('ad_id').count().alias('active_ads_count'),
            pl.col('price').min().alias('min_price'),
            pl.col('price').median().alias('median_price'),
            pl.col('price').max().alias('max_price'),
            pl.col('date').max().alias('last_recalculated_at'),
        )
    )

    if not market_baselines_df.is_empty():
        with Session(db_engine) as session:
            session.execute(
                insert(gold.FactMarketBaseline), market_baselines_df.to_dicts()
            )
            session.commit()
            print(f"Successfully calculated and persisted {len(market_baselines_df)} market baselines.")
    else:
        print("No baseline data found to insert.")


def run() -> None:
    """
    Synchronous entry point for market baselines pipeline execution.
    """
    run_market_baselines_pipeline()


if __name__ == "__main__":
    run()
