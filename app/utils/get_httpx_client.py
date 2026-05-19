import httpx


def get_httpx_client(base_url: str) -> httpx.AsyncClient:
    """
    Instantiates and returns an httpx.AsyncClient configured with custom limits and timeouts.

    Args:
        base_url (str): The base URL for the client.

    Returns:
        httpx.AsyncClient: The configured asynchronous HTTP client.
    """
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
        timeout=30
    )

    return client
