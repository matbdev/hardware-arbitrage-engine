"""
Gold Layer Arbitrage Opportunities Pipeline.
Evaluates clean listing prices against market baseline medians and product dimensions
to detect undervalued deals with high profit margins and opportunity scores.
"""
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
import polars as pl

from app.config import db_engine
from app.models import silver, gold


def run_arbitrage_opportunities_pipeline() -> None:
    """
    Executes the Gold layer arbitrage opportunity detection pipeline.
    """
    print("Running Gold Layer: Arbitrage Opportunities pipeline...")

    with db_engine.connect() as connection:
        # Active clean ad listings from Silver layer
        df_silver_raw = pl.read_database(
            select(
                silver.SilverCleanAd.ad_id,
                silver.SilverCleanAd.title,
                silver.SilverCleanAd.url,
                silver.SilverCleanAd.first_image_src,
                silver.SilverCleanAd.item_condition,
                silver.SilverCleanAd.price.label('current_price'),
                silver.SilverCleanAd.baseline_id,
                silver.SilverCleanAd.item_condition_indicator,
                silver.SilverCleanAd.urgent_sale.label('is_urgent_sale')
            ),
            connection=connection
        )

        # Product dimension table to retrieve specs_summary
        df_dim_products = pl.read_database(
            select(
                gold.DimProduct.baseline_id,
                gold.DimProduct.specs_summary
            ),
            connection=connection
        )

        # Market baseline benchmarks to retrieve market median price
        df_gold_baselines = pl.read_database(
            select(
                gold.FactMarketBaseline.baseline_id,
                gold.FactMarketBaseline.median_price.label('market_median_price')
            ),
            connection=connection
        )

    if df_silver_raw.is_empty() or df_gold_baselines.is_empty() or df_dim_products.is_empty():
        print("Insufficient data available across Silver or Gold baseline/dimension tables to evaluate arbitrage opportunities.")
        return

    # Join listings with product specs dimension and market baselines
    df_arbitrage_opportunities = (
        df_silver_raw
        .join(df_dim_products, on='baseline_id', how='inner')
        .join(df_gold_baselines, on='baseline_id', how='inner')
        .filter(pl.col('current_price') < pl.col('market_median_price'))
        .with_columns(
            (pl.col('market_median_price') - pl.col('current_price')).round(2).alias('potential_profit'),
            (((pl.col('market_median_price') - pl.col('current_price')) / pl.col('current_price') * 100)).round(2).alias('profit_margin_pct')
        )
        .with_columns(
            (
                pl.col('profit_margin_pct').clip(0, 100) * 0.7
                + pl.when(pl.col('is_urgent_sale')).then(20).otherwise(0)
                + pl.when(pl.col('item_condition_indicator') == 1).then(10)
                  .when(pl.col('item_condition_indicator') == 2).then(7)
                  .when(pl.col('item_condition_indicator') == 3).then(5)
                  .otherwise(0)
            ).clip(0, 100).round(1).alias('opportunity_score')
        )
        .drop('item_condition_indicator')
    )

    if not df_arbitrage_opportunities.is_empty():
        with Session(db_engine) as session:
            session.execute(
                insert(gold.FactArbitrageOpportunity), df_arbitrage_opportunities.to_dicts()
            )
            session.commit()
            print(f"Successfully detected and saved {len(df_arbitrage_opportunities)} arbitrage opportunities.")
    else:
        print("No arbitrage opportunities found.")


def run() -> None:
    """
    Synchronous entry point for arbitrage opportunities pipeline execution.
    """
    run_arbitrage_opportunities_pipeline()


if __name__ == "__main__":
    run()
