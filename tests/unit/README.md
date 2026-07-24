# Unit Tests (`tests/unit/`)

Contains fast, isolated unit tests for core utilities, regex data cleaners, HTML parsing services, and Pydantic schema validation without database or network I/O.

## Test Components

- **`test_pagination.py`**: Tests pagination utility functions (`calculate_offset`, `calculate_total_pages`, `build_paginated_response`).
- **`test_silver_cleaners.py`**: Tests column name sanitization (`clean_col_name`), regex spec extraction (RAM/Storage), and condition flag regex matching (`needs_repair`, `urgent_sale`).
- **`test_olx_service.py`**: Tests HTML string parsing (`OLXService.extract_further_information`) and price string to float conversion (`"R$ 1.800,00"` $\rightarrow$ `1800.0`).
- **`test_schemas.py`**: Tests Pydantic DTO schema validation rules and optional field handling (`first_image_src=None`).

## Execution

```bash
uv run pytest tests/unit/
```

## Related Links

- [Test Suite Overview](../README.md)
- [Integration Tests](../integration/README.md)
- [API Endpoint Tests](../api/README.md)
- [App Utilities](../../app/utils/README.md)
- [Silver Cleaning Pipeline](../../app/pipelines/silver/README.md)
