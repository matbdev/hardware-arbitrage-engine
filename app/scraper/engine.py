import logging

import httpx
from bs4 import BeautifulSoup
from tenacity import before_sleep_log, retry, stop_after_attempt, wait_exponential

# Tenacity
from ..config import logger


# Wait exponentially: 4s, 8s, 16s, 32s, up to 60s max.
# Stop trying after 6 total attempts.
# Log a message before sleeping so you know a 429 happened.
@retry(
    wait=wait_exponential(multiplier=2, min=4, max=60),
    stop=stop_after_attempt(6),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True # If it fails 6 times, raise the error to be caught
)
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

        return {'url': url, 'status': response.status_code, 'body': body, 'available': True}

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 410:
            print(f"Add {url} isn't available (selled/deleted).")
            return {'url': url, 'status': response.status_code, 'body': None, 'available': False}
        elif exc.response.status_code == 404:
            print(f"Page not found: {url}")
            return {'url': url, 'status': 404, 'body': None, 'avaliable': False}
        else:
            print(f"Unexpected error: {exc}")
            raise exc