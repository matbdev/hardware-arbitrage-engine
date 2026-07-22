"""
Bronze Layer Discovery Pipeline.
Discovers product search listing URLs from marketplaces (e.g., OLX) and saves raw links to the database.
"""
import asyncio

import polars as pl
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.config import db_engine
from app.models import GeneralSearch
from app.services import OLXCrawler
from app.utils import read_search_locations_metadata


async def run_discover_pipeline() -> None:
    """
    Executes the Bronze layer link discovery pipeline asynchronously.
    """
    general_data_rows = []

    # Load search location metadata
    brazil_data_location = (
        read_search_locations_metadata()
        .get('search_locations', {})
        .get('brazil', {})
    )

    stores = brazil_data_location.get('stores', [])
    if not stores:
        print("No store search locations configured.")
        return

    # For now, process the primary configured store (OLX)
    stores_to_process = [stores[0]]
    print(f"Stores to process in discovery: {[s.get('name') for s in stores_to_process]}")

    for store in stores_to_process:
        store_name = store.get('name', '')
        store_base_url = store.get('base_url', '')

        print(f"Processing store discovery: {store_name}")

        if store_name == 'OLX':
            olx_crawler = OLXCrawler(
                base_url=store_base_url,
                base_data_list=general_data_rows
            )
            await olx_crawler.scrap_general_links()

    # Create Polars DataFrame from discovered listings
    general_df = pl.DataFrame(general_data_rows)

    if not general_df.is_empty():
        print(f"Saving {len(general_df)} discovered listings to database...")
        with Session(db_engine) as session:
            session.execute(insert(GeneralSearch), general_df.to_dicts())
            session.commit()
            print("Discovery data successfully committed.")
    else:
        print("No discovery data found to insert.")


def run() -> None:
    """
    Synchronous entry point for discovery pipeline execution.
    """
    asyncio.run(run_discover_pipeline())


if __name__ == "__main__":
    run()
