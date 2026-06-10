import re
from bs4 import BeautifulSoup
from ..utils import get_httpx_client
from ..scraper import scrape_url

class OLXService:
    def __init__(self, base_url="https://www.olx.com.br"):
        """ 
        Initializes the OLXService with an asynchronous HTTP client.
        """
        self.http_client = get_httpx_client(base_url=base_url)

    async def get_details_links(self, item_name):
        """
        Fetches item details from OLX by scraping the search results page.
        
        Args:
            item_name (str): The name of the item to search for.
        
        Returns:
            dict: A dictionary containing the scraped data.
        """
        scrape_search_url = f"/brasil?q={item_name.replace(' ', '+')}"
        result = await scrape_url(scrape_search_url, self.http_client)
        
        if result.get("status") == 200 and "body" in result:
            soup = BeautifulSoup(result["body"], "html.parser")
            # Div starts with AdListing_adListContainer
            ad_container = soup.find("div", class_=re.compile(r"^AdListing_adListContainer"))

            # Takes all links from the ad container
            a_tags = ad_container.find_all("a", href=True) if ad_container else []
            links = [a["href"] for a in a_tags]
            
            if ad_container:
                return {
                    "url": result["url"],
                    "status": result["status"],
                    "links": links
                }
            else:
                return {
                    "url": result["url"],
                    "status": result["status"],
                    "error": "AdListing_adListContainer div not found"
                }
                
        return result

    async def terminate_client(self):
        """
        Closes the asynchronous HTTP client to free up resources.
        """
        await self.http_client.aclose()