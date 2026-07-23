"""
Configuration module for the Hardware Arbitrage Engine.
Sets up logging and establishes the database connection engine.
"""
import os
import asyncio
import logging
from pathlib import Path

from sqlalchemy import create_engine, URL

BASE_DIR = Path(__file__).resolve().parents[1]

# --- Logging Configuration ---
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- SQLAlchemy Configuration ---
def get_database_url():
    # Replace these with your exact environment variables and defaults
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_pass = os.getenv("POSTGRES_PASSWORD", "postgres")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "scraping_database")

    db_url_path = URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_pass,
        port=db_port,
        host=db_host,
        database=db_name,
        query={"sslmode": "prefer"}
    )

    # For alembic
    return db_url_path.render_as_string(hide_password=False)

db_engine = create_engine(get_database_url())

# --- Semaphore ---
semaphore = asyncio.Semaphore(3)