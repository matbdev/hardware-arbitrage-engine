"""
Gold Layer Product Dimension Pydantic Schema.
Data Transfer Object (DTO) for serving hardware product configurations and normalized specification summaries.
"""
from pydantic import BaseModel, ConfigDict, Field


class Product(BaseModel):
    """
    Pydantic schema for serializing 'dim_products' dimension data.
    """
    model_config = ConfigDict(from_attributes=True)

    # Primary key linking unique product baseline configurations
    baseline_id: str = Field(..., description="Unique product baseline identifier", example="lenovo_i7_16gb_512gb")
    
    # Product classification attributes
    category: str = Field(..., description="Hardware category classification", example="notebook")
    brand: str = Field(..., description="Product brand manufacturer name", example="Lenovo")
    cpu_brand: str = Field(..., description="CPU processor brand manufacturer", example="Intel")
    cpu_model: str = Field(..., description="Specific CPU processor model name", example="i7-10700K")
    ram_gb: int = Field(..., description="System RAM memory size in gigabytes", example=16)
    storage_gb: int = Field(..., description="System storage capacity in gigabytes", example=512)
    
    # Formatted summary of specifications (e.g., 'i7-10700K, 16GB RAM, 512GB SSD')
    specs_summary: str = Field(..., description="Formatted summary string of specs", example="Intel Core i7-10700K, 16GB RAM, 512GB SSD")
