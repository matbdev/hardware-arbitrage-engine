import asyncio
from unittest.mock import AsyncMock, patch

from app.services.olx_service import OLXService


def test_extract_further_information_html_parsing():
    mock_html_body = """
    <html>
        <body>
            <button id="item-gallery-image-0">
                <picture>
                    <img src="https://img.olx.com.br/images/99/99123.jpg" />
                </picture>
            </button>
            <div id="description-title">
                <span>Lenovo ThinkPad i7 16GB</span>
                <div data-section="description">
                    <span class="typo-body-medium">Notebook em otimo estado de conservacao</span>
                </div>
            </div>
            <div id="price-box-container">
                <span>R$ 1.800,00</span>
            </div>
            <div id="ad-favorite-modal">
                <a href="https://olx.com.br/favorite?ad_id=987654321">Favoritar</a>
            </div>
            <div id="details">
                <div class="olx-container">
                    <span>Categoria</span>
                    <span>Computadores e acessorios</span>
                </div>
            </div>
        </body>
    </html>
    """

    mock_response = {
        "status": 200,
        "body": mock_html_body
    }

    async def run_test():
        service = OLXService()
        with patch("app.services.olx_service.scrape_url", new_callable=AsyncMock) as mock_scrape:
            mock_scrape.return_value = mock_response

            result = await service.extract_further_information("https://olx.com.br/vi/987654321")

            assert result["title"] == "Lenovo ThinkPad i7 16GB"
            assert result["price"] == 1800.0
            assert result["currency"] == "R$"
            assert result["first_image"] == "https://img.olx.com.br/images/99/99123.jpg"
            assert result["ad_id"] == "987654321"

        await service.terminate_client()

    asyncio.run(run_test())
