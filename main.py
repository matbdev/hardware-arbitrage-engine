"""
Main entry point for the Hardware Arbitrage Engine application.
Initializes environment variables, creates database tables, and executes the data pipeline.
"""
from dotenv import load_dotenv


def main() -> None:
    """
    Main application runner function.
    """
    # Load environment variables from .env file if present
    load_dotenv()

    # Execute full data pipeline across Bronze, Silver, and Gold layers
    # print("Starting pipeline execution...")
    # run_pipelines()
    # print("Pipeline execution completed successfully.")


if __name__ == "__main__":
    main()
