import httpx
from bs4 import BeautifulSoup

from ..utils import get_httpx_client


async def scrape_url(url: str, client: httpx.AsyncClient) -> dict:
    """
    Scrapes a website asynchronously.

    Args:
        url (str): The URL to scrape.
        client (httpx.AsyncClient): The async HTTP client.

    Returns:
        dict: The scraped data.
    """
    # Asynchronously fetch the page content
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        body = str(soup.body) if soup.body else 'No Body Found'

        return {'url': url, 'status': response.status_code, 'body': body}

    except Exception as e:
        print(f'Error: {e}')
        return {'url': url, 'status': 'error', 'title': str(e)}
