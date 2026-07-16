import httpx


def get_httpx_client(base_url: str) -> httpx.AsyncClient:
    """
    Instantiates and returns an httpx.AsyncClient configured with custom limits and timeouts.

    Args:
        base_url (str): The base URL for the client.

    Returns:
        httpx.AsyncClient: The configured asynchronous HTTP client.
    """
    # HTTP headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }

    # HTTP client limit
    limits = httpx.Limits(
        max_connections=100,
        max_keepalive_connections=20
    )

    # HTTP client instantiation
    client = httpx.AsyncClient(
        base_url=base_url,
        limits=limits,
        follow_redirects=True,
        timeout=30,
        headers=headers,
        http2=False,
        verify=False
    )

    return client
