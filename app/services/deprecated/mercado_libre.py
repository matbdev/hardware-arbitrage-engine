from ..utils import get_httpx_client
import time
import httpx
import os

class MercadoLibreService:
    def __init__(self):
        self.http_client = get_httpx_client(base_url="https://api.mercadolibre.com")
        self._cached_token = None
        self._token_expires_at = 0
        self.client_id = os.getenv("MERCADO_LIBRE_CLIENT_ID", "")
        self.client_secret = os.getenv("MERCADO_LIBRE_CLIENT_SECRET", "")

    async def _get_access_token(self):
        """
        Fetches an access token from the Mercado Libre API using client credentials.

        Returns:
            str: The access token.
        """
        # If the token is cached and not expired, return it
        if self._cached_token and time.time() < self._token_expires_at:
            return self._cached_token

        auth_url = "/oauth/token"
    
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        # Gets the access token and returns it
        try:
            response = await self.http_client.post(auth_url, data=payload)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP status error: {e.response.status_code}")
            print(f"Body: {e.response.text}")
            raise e
        except httpx.RequestError as e:
            print(f"Request error: {e}")
            raise e

        self._cached_token = data.get("access_token")
        self._token_expires_at = time.time() + data.get("expires_in", 21600) - 300

        return self._cached_token

    async def get_item_details(self, item: str, limit: int = 10):
        """
        Fetches item details from the Mercado Libre API.

        Args:
            item (str): The item to fetch details for.
            limit (int): The maximum number of results to return.
        """
        access_token = await self._get_access_token()
        search_url = "/sites/MLB/search"

        # Sets the query parameters for the request
        params = {"q": item, "limit": limit}

        # Adds the access token to the default headers
        self.http_client.headers.update({"Authorization": f"Bearer {access_token}"})

        try:
            # Makes the request to the Mercado Libre API and returns the response data
            response = await self.http_client.get(search_url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP status error: {e.response.status_code}")
            print(f"Body: {e.response.text}")
            raise e
        except httpx.RequestError as e:
            print(f"Request error: {e}")
            raise e

    async def terminate_client(self):
        """
        Terminates the HTTP client.
        """
        await self.http_client.aclose()