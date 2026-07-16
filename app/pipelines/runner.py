"""
Pipeline orchestrator module.
Provides functions to trigger the execution of Papermill notebooks for each data layer.
"""
import papermill as pm
from pathlib import Path

def run_pipelines():
    """
    Executes the full data pipeline across Bronze, Silver, and Gold layers.
    """
    base_path = Path.cwd()
    bronze_path = base_path / 'bronze'
    silver_path = base_path / 'silver'
    gold_path = base_path / 'gold'

    run_bronze_pipeline(bronze_path)

def run_bronze_pipeline(bronze_path: Path):
    """
    Executes the Bronze layer notebooks (discover and extraction) using Papermill.
    
    Args:
        bronze_path (Path): The path to the bronze layer directory containing the notebooks.
    """
    # Run the discover notebook
    pm.execute_notebook(bronze_path / 'discover.ipynb')
    # Run the extraction notebook
    pm.execute_notebook(bronze_path / 'extraction.ipynb')