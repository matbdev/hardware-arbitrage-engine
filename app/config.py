"""
Configuration module for the Hardware Arbitrage Engine.
Sets up logging and establishes the database connection engine.
"""
import asyncio
import logging
from pathlib import Path

from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parents[1]

# --- Logging Configuration ---
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- SQLAlchemy Configuration ---
db_path = BASE_DIR / 'scraping_database.db'
db_engine = create_engine(f'sqlite:///{db_path}')

# --- Semaphore ---
semaphore = asyncio.Semaphore(3)