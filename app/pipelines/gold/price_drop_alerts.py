"""
Gold Layer Price Drop Alerts Pipeline.
Monitors price variations over time per ad listing and flags price drop alerts.
"""
import polars as pl
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.config import db_engine
from app.models import gold, silver


def run_price_drop_alerts_pipeline() -> None:
    """
    Executes the Gold layer price drop alert monitoring pipeline.
    """
    print("Running Gold Layer: Price Drop Alerts pipeline...")

    with db_engine.connect() as connection:
        df_silver_raw = pl.read_database(
            select(
                silver.SilverCleanAd.ad_id,
                silver.SilverCleanAd.title,
                silver.SilverCleanAd.url,
                silver.SilverCleanAd.price,
                silver.SilverCleanAd.date
            ),
            connection=connection
        )

    if df_silver_raw.is_empty():
        print("No Silver clean ads data available for price drop alerts.")
        return

    # Track price drop variations per ad listing over time
    df_price_drop_alerts = (
        df_silver_raw
        .sort(['ad_id', 'date'])
        .group_by('ad_id')
        .agg(
            pl.col('title').last().alias('title'),
            pl.col('url').last().alias('url'),
            pl.col('price').first().alias('initial_price'),
            pl.col('price').last().alias('current_price'),
            pl.col('date').first().alias('first_seen_date'),
            pl.col('date').last().alias('last_seen_date')
        )
        .filter(pl.col('initial_price') != pl.col('current_price'))
        .with_columns(
            (pl.col('last_seen_date') - pl.col('first_seen_date')).dt.total_days().cast(pl.Int32).alias('days_on_market'),
            (((pl.col('current_price') - pl.col('initial_price')) / pl.col('initial_price')) * 100).round(2).alias('price_change_pct')
        )
        .drop(['first_seen_date', 'last_seen_date'])
    )

    if not df_price_drop_alerts.is_empty():
        with Session(db_engine) as session:
            session.execute(
                insert(gold.FactPriceDropAlert), df_price_drop_alerts.to_dicts()
            )
            session.commit()
            print(f"Successfully recorded and persisted {len(df_price_drop_alerts)} price drop alerts.")
    else:
        print("No price drop alerts found.")


def run() -> None:
    """
    Synchronous entry point for price drop alerts pipeline execution.
    """
    run_price_drop_alerts_pipeline()


if __name__ == "__main__":
    run()
