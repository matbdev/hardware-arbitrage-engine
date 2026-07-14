import logging
from sqlalchemy import create_engine

# --- Logging ---
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- SQLAlchemy ---
db_engine = create_engine('sqlite:///scraping_database.db')