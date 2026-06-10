from dotenv import load_dotenv

from .services import OLXService
from .utils import (
    read_search_locations_metadata,
    read_scraping_targets_metadata,
    read_additional_info_metadata
)

# Loads env variables from .env file
load_dotenv()

async def main():
    olx_service = OLXService()

    # Read the scraping targets metadata
    targets_metadata = read_scraping_targets_metadata().get("targets", [])
    itens = targets_metadata.items()

    for category, subcategories in itens:
        # print(f"Category: {category}")

        for subcategory, items in subcategories.items():
            append_subcategory = False
            if category in ["memory", "storage", "peripherals"]:
                append_subcategory = True
            if subcategory in ["motherboard"]:
                append_subcategory = True
            
            # print(f"Subcategory: {subcategory}")
            for item in items:
                item_name = item.get('pt', '')
                if append_subcategory or item_name == "":
                    item_name = subcategory.capitalize() + " " + item_name
                    results = await olx_service.get_details_links(item_name)
                    print(results)
                # print(f"Item: {item_name}")
            print()
        print()

    await olx_service.terminate_client()
