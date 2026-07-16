import re
import asyncio
import random
import polars as pl
from app.services import OLXService
from app.utils import read_scraping_targets_metadata
from app.config import semaphore

# Regex pattern to extract region from OLX URLs
OLX_REGION_PATTERN = re.compile(r"https?://([^.]+)\.olx")

class OLXCrawler:
    """
    Crawler responsible for discovering and extracting product links from OLX.
    This class orchestrates the interaction with OLXService and applies business rules
    based on the project's scraping targets.
    """
    def __init__(self, base_data_list: list, base_url: str = "https://www.olx.com.br"):
        """
        Initializes the crawler.

        Args:
            base_data_list (list): The list where extracted row dictionaries will be appended.
            base_url (str, optional): The base URL of the store. Defaults to "https://www.olx.com.br".
        """
        self.olx_service = OLXService(base_url=base_url)
        self.base_data_list = base_data_list
    
    async def scrap_general_links(self):
        """
        Starts the scraping process to discover general links and terminates the client afterwards.
        """
        await self.search_for_general_links()
        await self.olx_service.terminate_client()

    async def scrap_specific_information(self, df: pl.DataFrame, not_available_products: list):
        """
        Starts the scraping process to discover specific product information and terminates the client afterwards.

        Args:
            df (pl.DataFrame): DataFrame containing links and metadata of products to be scraped.
            not_available_products (list): A list where unavailable product IDs will be appended.
        """
        await self.scrap_for_specific_information(
            df=df,
            not_available_products=not_available_products
        )
        await self.olx_service.terminate_client()

    async def search_for_general_links(self):
        """
        Reads target metadata (categories and subcategories), queries the OLX service,
        and populates the base_data_list with the discovered items and their links.
        This represents the primary discovery flow for the Bronze layer.
        """
        # Read the scraping targets metadata
        targets_metadata = read_scraping_targets_metadata().get("targets", [])
        itens = targets_metadata.items()

        # Tasks arguments for semaphore execution
        tasks_args = []
        for category, subcategories in itens:
            for subcategory, items in subcategories.items():
                append_subcategory = False
                if category in ["memory", "storage", "peripherals"]:
                    append_subcategory = True
                if subcategory in ["motherboard"]:
                    append_subcategory = True
                
                for item in items:
                    item_name = item.get('pt', '')
                    if append_subcategory or item_name == "":
                        item_name = subcategory.capitalize() + " " + item_name

                    tasks_args.append((category, subcategory, item_name))
        
        # 2. Define Semaphore and Async Worker
        async def fetch_general(category, subcategory, item_name):
            async with semaphore:
                # Delay between runs, 0.5 - 1.5s
                await asyncio.sleep(random.uniform(0.5, 1.5))
                results = await self.olx_service.get_details_links(item_name)
                return category, subcategory, item_name, results
        
        # 3. Concurrent Execution
        tasks = [fetch_general(c, s, i) for c, s, i in tasks_args]
        completed_tasks = await asyncio.gather(*tasks)

        # 4. Results Processing
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
        Iterates over a DataFrame of target products and queries the OLX service to extract specific information.
        Populates the base_data_list with the extracted details and updates not_available_products if applicable.

        Args:
            df (pl.DataFrame): DataFrame containing product information like general_search_id, link, and store.
            not_available_products (list): A list where unavailable product IDs will be appended.
        """

        # 1. Define Semaphore and Async Worker
        async def fetch_specific(row):
            async with semaphore:
                # Delay between runs, 0.5 - 2s
                await asyncio.sleep(random.uniform(0.5, 2.0))
                general_search_id = row[0]
                link = row[7]

                result = await self.olx_service.extract_further_information(link)
                return general_search_id, result

        # 2. Concurrent Execution based on Polars DataFrame rows
        tasks = [fetch_specific(row) for row in df.iter_rows()]
        completed_tasks = await asyncio.gather(*tasks)

        # 3. Results Processing and Separation
        for general_search_id, result in completed_tasks:
            # If is not available (410), insert into another table for future update
            if "available" in result:
                not_available_products.append({
                    "id": general_search_id,
                    "available": result["available"]
                })
            else:
                # Otherwise, insert into the extraction table
                self.base_data_list.append({
                    "general_search_id": general_search_id,
                    "first_image_src": result['first_image'],
                    "title": result['title'],
                    "description": result['description'],
                    "price": result['price'],
                    "currency": result['currency'],
                    "specifications": result['details_dict']
                })