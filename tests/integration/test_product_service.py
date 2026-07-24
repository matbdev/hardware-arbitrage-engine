from app.models.gold import DimProduct
from app.services.product_service import get_products_by_baseline_id


def test_get_products_by_baseline_id(db_session):
    product1 = DimProduct(
        baseline_id="b1",
        category="notebook",
        brand="Lenovo",
        cpu_brand="Intel",
        cpu_model="i7-10700K",
        ram_gb=16,
        storage_gb=512,
        specs_summary="i7, 16GB, 512GB"
    )
    product2 = DimProduct(
        baseline_id="b2",
        category="notebook",
        brand="Dell",
        cpu_brand="Intel",
        cpu_model="i5-1135G7",
        ram_gb=8,
        storage_gb=256,
        specs_summary="i5, 8GB, 256GB"
    )
    db_session.add_all([product1, product2])
    db_session.commit()

    # Filter by baseline_id="b1"
    result = get_products_by_baseline_id(db_session, baseline_id="b1", limit=10, page=1)
    assert result["total"] == 1
    assert result["items"][0].baseline_id == "b1"
