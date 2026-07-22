import re

from bs4 import BeautifulSoup

from ..scraper import scrape_url
from ..utils import get_httpx_client


class OLXService:
    def __init__(self, base_url="https://www.olx.com.br"):
        """ 
        Initializes the OLXService with an asynchronous HTTP client.

        Args:
            base_url (str, optional): The base URL of the store. Defaults to "https://www.olx.com.br".
        """
        self.http_client = get_httpx_client(base_url=base_url)

    async def get_details_links(self, item_name):
        """
        Fetches item details from OLX by scraping the search results page.
        
        Args:
            item_name (str): The name of the item to search for.
        
        Returns:
            dict: A dictionary containing the original URL, status code, and extracted links or error message.
        """
        scrape_search_url = f"/brasil?q={item_name.replace(' ', '+')}"
        result = await scrape_url(scrape_search_url, self.http_client)

        if not result:
            return {"url": scrape_search_url, "status": 500, "error": "Scraper returned None"}
        
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

    async def extract_further_information(self, link):
        """
        Fetches further item details from OLX by scraping the specific product page.
        
        Args:
            link (str): The product URL to scrape.
        
        Returns:
            dict: A dictionary containing the scraped data (e.g., first image, title, description, price, currency, details) or availability status.
        """
        result = await scrape_url(link, self.http_client)

        if result.get("status") == 410:
            return {"available": result.get("available")}

        if result.get("status") == 200 and "body" in result:
            soup = BeautifulSoup(result["body"], "html.parser")

            # Picture is set under button#item-gallery-image-{number} picture img
            pictures_button = soup.find("button", id=re.compile(r"^item-gallery-image"))
            picture_container = pictures_button.find("picture") if pictures_button else None
            first_image_tag = picture_container.find("img") if picture_container else None
            first_image_src = first_image_tag['src'] if first_image_tag else None

            # Title is set under div#description-title span.typo-title-medium
            description_title_div = soup.find("div", id="description-title")
            title_span = description_title_div.find("span") if description_title_div else None
            title = title_span.text if title_span else None

            # Description is set under div#description-title [data-section="description"] span
            description_section = description_title_div.find(attrs={"data-section": "description"})
            description_span = description_section.find("span", class_="typo-body-medium") if description_section else None
            description = description_span.text if description_span else None

            # Price is set under div#price-box-container .typo-title-large, in 'currency value' format
            price_container = soup.find("div", id="price-box-container")
            price_span = price_container.find("span") if price_container else None
            price_str = price_span.text if price_span else None

            # Initialize default values
            final_price = None
            final_currency = None

            if price_str:
                # E.g., splitting "R$ 1.500,00" -> ["R$", "1.500,00"]
                price_splitted = price_str.split(' ')
                
                if len(price_splitted) >= 2:
                    final_currency = price_splitted[0]
                    raw_value = price_splitted[1]
                    
                    # Remove the thousands separator (dot)
                    # Replace the decimal separator (comma) with a dot
                    clean_value = raw_value.replace('.', '').replace(',', '.')
                    
                    try:
                        final_price = float(clean_value)
                    except ValueError:
                        final_price = None

            # Details is set under div#details, with classes olx-container
            details_container = soup.find("div", id="details")
            details_divs = details_container.find_all("div", class_="olx-container") if details_container else None

            details_dict = {}

            # The unique ad id is located 'Add to favorites' modal, to remember the product you wanted
            # to interact with
            div_favorite = soup.find("div", id="ad-favorite-modal")
            ad_id = div_favorite.find("a").get('href').split('=')[-1] if div_favorite else None
            
            for div in details_divs:
                span_tags = div.find_all("span")

                if span_tags:
                    a_tag = None
                    if len(span_tags) < 2:
                        a_tag = div.find("a")
                        details_dict.update({span_tags[0].text: a_tag.text})
                    else:
                        details_dict.update({span_tags[0].text: span_tags[1].text})

            return {
                "first_image": first_image_src,
                "title": title,
                "description": description,
                "price": final_price,
                "currency": final_currency,
                "details_dict": details_dict,
                "ad_id": ad_id
            }

        return result

    async def terminate_client(self):
        """
        Closes the asynchronous HTTP client to free up resources.
        """
        await self.http_client.aclose()