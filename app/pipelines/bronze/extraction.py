"""
Bronze Layer Extraction Pipeline.
Extracts detailed product specifications, titles, descriptions, and prices for discovered links,
and saves the raw details to the InformationExtraction table.
"""
import asyncio

import polars as pl
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from app.config import db_engine
from app.models import GeneralSearch, InformationExtraction
from app.services import OLXCrawler
from app.utils import read_search_locations_metadata


async def run_extraction_pipeline() -> None:
    """
    Executes the Bronze layer detailed extraction pipeline asynchronously.
    """
    extraction_data_list = []
    not_available_products = []

    # Read location metadata for region filtering
    brazil_data_location = (
        read_search_locations_metadata()
        .get('search_locations', {})
        .get('brazil', {})
    )

    regions = brazil_data_location.get('regions', [])
    abbreviation_list = [region.get('abreviation') for region in regions]

    # Query general search links filtered by region and store
    with db_engine.connect() as connection:
        df_olx = pl.read_database(
            select(GeneralSearch).where(
                (GeneralSearch.region.in_(abbreviation_list))
                & (GeneralSearch.store.is_('OLX'))
            ),
            connection=connection
        )

    if df_olx.is_empty():
        print("No general search listings found for extraction.")
        return

    # Limit batch size for extraction run
    df_olx_batch = df_olx.head(100)
    print(f"Extracting detailed info for batch of {len(df_olx_batch)} listings...")

    olx_crawler = OLXCrawler(base_data_list=extraction_data_list)
    await olx_crawler.scrap_specific_information(
        df=df_olx_batch,
        not_available_products=not_available_products
    )

    # Convert results into Polars DataFrames
    extraction_data_df = pl.DataFrame(extraction_data_list)
    updated_df = pl.DataFrame(not_available_products)

    # Persist results to SQLite database
    if not extraction_data_df.is_empty():
        with Session(db_engine) as session:
            # Insert newly extracted detailed listing data
            session.execute(
                insert(InformationExtraction),
                extraction_data_df.to_dicts()
            )

            # Update availability status for deleted/sold items
            if not updated_df.is_empty():
                session.execute(
                    update(GeneralSearch),
                    updated_df.to_dicts()
                )
                print(f"Updated status for {len(updated_df)} unavailable items.")
            else:
                print("No unavailable item status updates required.")

            session.commit()
            print("Extraction data successfully committed.")
    else:
        print("No extraction data found to insert.")


def run() -> None:
    """
    Synchronous entry point for extraction pipeline execution.
    """
    asyncio.run(run_extraction_pipeline())


if __name__ == "__main__":
    run()
