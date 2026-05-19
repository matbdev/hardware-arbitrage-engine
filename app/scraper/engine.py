from bs4 import BeautifulSoup
from ..utils import get_httpx_client

async def scrape_site(url: str):
    """
    Scrapes a website asynchronously.

    Args:
        url (str): The URL to scrape.

    Returns:
        dict: The scraped data.
    """
    client = get_httpx_client(url)

    # Asynchronously fetch the page content
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title Found'

        return {'url': url, 'status': response.status_code, 'title': title.strip()}

    except Exception as e:
        print(f'Error: {e}')
        return {'url': url, 'status': 'error', 'title': str(e)}
