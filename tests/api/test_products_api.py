from app.models.gold import DimProduct


def test_get_products_endpoint_returns_paginated_response(client, db_session):
    product = DimProduct(
        baseline_id="b1",
        category="notebook",
        brand="Asus",
        cpu_brand="AMD",
        cpu_model="Ryzen 7 5700U",
        ram_gb=16,
        storage_gb=512,
        specs_summary="Ryzen 7, 16GB, 512GB"
    )
    db_session.add(product)
    db_session.commit()

    response = client.get("/api/v1/products/?baseline_id=b1&page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["brand"] == "Asus"
