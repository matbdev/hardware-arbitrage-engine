from pathlib import Path

import yaml

# Path to the metadata directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
METADATA_DIR = BASE_DIR / 'metadata'


def _read_yaml(file: Path) -> dict:
    """
    Reads a YAML file.

    Args:
        file (Path): The path to the YAML file.

    Returns:
        dict: The YAML data.
    """
    with open(file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def read_search_locations_metadata() -> dict:
    """
    Reads the search locations metadata from the YAML file.

    Returns:
        dict: The search locations metadata.
    """
    return _read_yaml(METADATA_DIR / 'search_locations.yml')


def read_scraping_targets_metadata() -> dict:
    """
    Reads the scraping targets metadata from the YAML file.

    Returns:
        dict: The scraping targets metadata.
    """
    return _read_yaml(METADATA_DIR / 'scraping_targets.yml')


def read_additional_info_metadata() -> dict:
    """
    Reads the additional information metadata from the YAML file.

    Returns:
        dict: The additional information metadata.
    """
    return _read_yaml(METADATA_DIR / 'additional_info.yml')

