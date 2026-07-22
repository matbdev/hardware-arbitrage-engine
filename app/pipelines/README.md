# Pipelines Package (`app/pipelines/`)

Orchestrates production ETL pipeline execution across Bronze, Silver, and Gold layers.

## Package Architecture

- **`runner.py`**: Master orchestrator script (`run_pipelines()`). Executes Bronze, Silver, and Gold pipelines sequentially in strict data dependency order.
- **[`bronze/`](bronze/README.md)**: Product search link discovery and detailed page extraction.
- **[`silver/`](silver/README.md)**: Raw data cleaning, regex feature flagging, and one-hot encoding.
- **[`gold/`](gold/README.md)**: Product dimension upsert, baseline pricing, market trends, price drop alerts, and deal arbitrage evaluation.

## Related Links
- [App Models](../models/README.md)
- [Scraper Engine](../scraper/README.md)
