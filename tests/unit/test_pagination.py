from app.utils.pagination import (
    build_paginated_response,
    calculate_offset,
    calculate_total_pages,
)


def test_calculate_offset_first_page():
    assert calculate_offset(page=1, limit=20) == 0


def test_calculate_offset_subsequent_page():
    assert calculate_offset(page=3, limit=20) == 40


def test_calculate_offset_handles_invalid_page():
    assert calculate_offset(page=0, limit=20) == 0


def test_calculate_total_pages():
    assert calculate_total_pages(total_items=45, limit=20) == 3
    assert calculate_total_pages(total_items=0, limit=20) == 1


def test_build_paginated_response():
    items = [{"id": 1}, {"id": 2}]
    response = build_paginated_response(
        items=items,
        total_items=45,
        page=1,
        limit=20
    )
    assert response["total"] == 45
    assert response["page"] == 1
    assert response["limit"] == 20
    assert response["total_pages"] == 3
    assert response["items"] == items