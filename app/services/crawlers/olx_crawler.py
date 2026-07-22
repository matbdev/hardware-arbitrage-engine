"""
OLX Crawler module for discovering and extracting product listings from OLX marketplace.
"""
import asyncio
import random
import re

import polars as pl

from app.config import semaphore
from app.services.olx_service import OLXService
from app.utils import read_scraping_targets_metadata

# Regex pattern to extract region from OLX URLs
OLX_REGION_PATTERN = re.compile(r"https?://([^.]+)\.olx")

class OLXCrawler:
    """
    Crawler responsible for discovering and extracting product links from OLX.
    Orchestrates interaction with OLXService and applies business rules
    based on the project's scraping targets.
    """
    def __init__(self, base_data_list: list, base_url: str = "https://www.olx.com.br"):
        """
        Initializes the OLX crawler.

        Args:
            base_data_list (list): Reference list to append extracted row dictionaries.
            base_url (str, optional): Base URL of the store. Defaults to "https://www.olx.com.br".
        """
        self.olx_service = OLXService(base_url=base_url)
        self.base_data_list = base_data_list
    
    async def scrap_general_links(self):
        """
        Starts the scraping process to discover general links and terminates the HTTP client afterwards.
        """
        await self.search_for_general_links()
        await self.olx_service.terminate_client()

    async def scrap_specific_information(self, df: pl.DataFrame, not_available_products: list):
        """
        Starts the scraping process for specific product details and terminates the client afterwards.

        Args:
            df (pl.DataFrame): DataFrame containing links and metadata of products to be scraped.
            not_available_products (list): Reference list to append unavailable product IDs.
        """
        await self.scrap_for_specific_information(
            df=df,
            not_available_products=not_available_products
        )
        await self.olx_service.terminate_client()

    async def search_for_general_links(self):
        """
        Reads target metadata (categories and subcategories), queries the OLX service,
        and populates base_data_list with discovered items and links.
        Represents the primary discovery flow for the Bronze layer.
        """
        # Read the scraping targets metadata
        targets_metadata = read_scraping_targets_metadata().get("targets", [])
        items = targets_metadata.items()

        # Task arguments for semaphore execution
        tasks_args = []
        for category, subcategories in items:
            for subcategory, item_list in subcategories.items():
                append_subcategory = False
                if category in ["memory", "storage", "peripherals"]:
                    append_subcategory = True
                if subcategory in ["motherboard"]:
                    append_subcategory = True
                
                for item in item_list:
                    item_name = item.get('pt', '')
                    if append_subcategory or item_name == "":
                        item_name = subcategory.capitalize() + " " + item_name

                    tasks_args.append((category, subcategory, item_name))
        
        # Define Semaphore and Async Worker
        async def fetch_general(category, subcategory, item_name):
            async with semaphore:
                # Random delay between runs (0.5 - 1.5s) to avoid rate limits
                await asyncio.sleep(random.uniform(0.5, 1.5))
                results = await self.olx_service.get_details_links(item_name)
                return category, subcategory, item_name, results
        
        # Concurrent Execution
        tasks = [fetch_general(c, s, i) for c, s, i in tasks_args]
        completed_tasks = await asyncio.gather(*tasks)

        # Results Processing
        for category, subcategory, item_name, results in completed_tasks:
            url = results.get('url', '')
            status = results.get('status', 400)
            links = results.get('links', [])
            
            if status != 200:
                print(f'Error processing url: {url}')

            for link in links:
                if link:
                    # Extract region from link
                    match = OLX_REGION_PATTERN.search(link)
                    region = match.group(1) if match else "unknown"

                    self.base_data_list.append({
                        'category': category,
                        'subcategory': subcategory,
                        'item': item_name,
                        'url': url,
                        'status': status,
                        'region': region,
                        'link': link,
                        'store': 'OLX'
                    })

    async def scrap_for_specific_information(self, df: pl.DataFrame, not_available_products: list):
        """
        Iterates over a DataFrame of target products and queries OLX service for detailed info.
        Populates base_data_list with extracted details and updates not_available_products if applicable.

        Args:
            df (pl.DataFrame): DataFrame containing product information (id, link, etc.).
            not_available_products (list): Reference list for unavailable product IDs.
        """

        # Define Semaphore and Async Worker
        async def fetch_specific(row):
            async with semaphore:
                # Random delay between runs (0.5 - 2.0s)
                await asyncio.sleep(random.uniform(0.5, 2.0))
                general_search_id = row[0]
                link = row[7]

                result = await self.olx_service.extract_further_information(link)
                return general_search_id, result

        # Concurrent Execution based on Polars DataFrame rows
        tasks = [fetch_specific(row) for row in df.iter_rows()]
        completed_tasks = await asyncio.gather(*tasks)

        # Results Processing and Separation
        for general_search_id, result in completed_tasks:
            # If not available (410 Gone / deleted), insert into unavailable list
            if "available" in result:
                not_available_products.append({
                    "id": general_search_id,
                    "available": result["available"]
                })
            else:
                # Insert into extraction dataset
                self.base_data_list.append({
                    "general_search_id": general_search_id,
                    "first_image_src": result['first_image'],
                    "title": result['title'],
                    "description": result['description'],
                    "price": result['price'],
                    "currency": result['currency'],
                    "specifications": result['details_dict'],
                    "ad_id": result['ad_id']
                })
