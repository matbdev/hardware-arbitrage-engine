"""
Gold Layer Product Dimension Pipeline.
Extracts unique product hardware configurations from Silver layer clean ads
and populates/upserts the dim_products table.
"""
from sqlalchemy import cast, func, select, String
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session
import polars as pl

from app.config import db_engine
from app.models import silver, gold


def run_dim_products_pipeline() -> None:
    """
    Executes the Gold layer product dimension extraction and upsert pipeline.
    """
    print("Running Gold Layer: Product Dimensions pipeline...")

    with db_engine.connect() as connection:
        df_silver_products = pl.read_database(
            select(
                silver.SilverCleanAd.baseline_id,
                silver.SilverCleanAd.category,
                silver.SilverCleanAd.brand,
                silver.SilverCleanAd.cpu_brand,
                silver.SilverCleanAd.cpu_model,
                silver.SilverCleanAd.ram_gb,
                silver.SilverCleanAd.storage_gb,
                func.concat_ws(
                    ', ', 
                    func.nullif(silver.SilverCleanAd.cpu_model, 'Brand Not Informed'),
                    cast(func.nullif(silver.SilverCleanAd.ram_gb, 0), String) + 'GB RAM',
                    cast(func.nullif(silver.SilverCleanAd.storage_gb, 0), String) + 'GB SSD'
                ).label('specs_summary')
            )
            .where(silver.SilverCleanAd.baseline_id.is_not(None)),
            connection=connection
        )

    if df_silver_products.is_empty():
        print("No Silver clean ads found for product dimension pipeline.")
        return

    # Deduplicate product configurations by baseline_id
    df_dim_products = df_silver_products.unique(subset=['baseline_id'], keep='first')

    if not df_dim_products.is_empty():
        with Session(db_engine) as session:
            stmt = sqlite_insert(gold.DimProduct).values(df_dim_products.to_dicts())
            stmt = stmt.on_conflict_do_nothing(index_elements=['baseline_id'])
            session.execute(stmt)
            session.commit()
            print(f"Successfully upserted {len(df_dim_products)} records into dim_products.")
    else:
        print("No new product dimension data to persist.")


def run() -> None:
    """
    Synchronous entry point for product dimensions pipeline execution.
    """
    run_dim_products_pipeline()


if __name__ == "__main__":
    run()
