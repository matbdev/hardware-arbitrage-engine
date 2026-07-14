from typing import Optional
from datetime import datetime
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class GeneralSearch(Base):
    __tablename__ = "general_search"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    subcategory: Mapped[str]
    item: Mapped[str]
    url: Mapped[str]
    status: Mapped[int]
    links: Mapped[Optional[list[str]]] = mapped_column(JSON)
    datetime: Mapped[datetime]