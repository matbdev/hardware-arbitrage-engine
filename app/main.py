from dotenv import load_dotenv

from .utils import (
    read_additional_info_metadata,
    read_scraping_targets_metadata,
    read_search_locations_metadata,
)

# Loads env variables from .env file
load_dotenv()

def main():
    # Reading metadata
    additinal_info = read_additional_info_metadata()
    scraping_targets = read_scraping_targets_metadata()
    search_locations = read_search_locations_metadata()

    print('Additional Info\n')
    print(additinal_info)
    print('\nScraping Targets\n')
    print(scraping_targets)
    print('\nSearch Locations\n')
    print(search_locations)