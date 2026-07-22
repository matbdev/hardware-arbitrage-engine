from typing import Optional
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class InformationExtraction(Base):
    """
    SQLAlchemy model representing the 'bronze_extraction_data' table.
    Stores the result of the scrap of the links collected and saved following the above schema
    """
    __tablename__ = "bronze_extraction_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    ad_id: Mapped[str]
    general_search_id: Mapped[int]
    first_image_src: Mapped[str]
    title: Mapped[str]
    description: Mapped[Optional[str]]
    currency: Mapped[Optional[str]]
    price: Mapped[Optional[float]]
    specifications: Mapped[Optional[dict[str, str]]] = mapped_column(JSON)
