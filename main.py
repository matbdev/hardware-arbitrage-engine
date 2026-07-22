"""
Main entry point for the Hardware Arbitrage Engine application.
Initializes environment variables, creates database tables, and executes the data pipeline.
"""
from dotenv import load_dotenv

from app.config import db_engine
from app.models import Base
from app.pipelines import run_pipelines


def main() -> None:
    """
    Main application runner function.
    """
    # Load environment variables from .env file if present
    load_dotenv()

    # Create all ORM mapped database tables if they do not exist
    print("Initializing database tables...")
    Base.metadata.create_all(db_engine)
    print("Database tables initialized successfully.")

    # Execute full data pipeline across Bronze, Silver, and Gold layers
    # print("Starting pipeline execution...")
    # run_pipelines()
    # print("Pipeline execution completed successfully.")


if __name__ == "__main__":
    main()
