from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class GeneralSearch(Base):
    __tablename__ = "bronze_ad_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    subcategory: Mapped[str]
    item: Mapped[str]
    url: Mapped[str]
    status: Mapped[int]
    region: Mapped[str]
    link: Mapped[str]
    datetime: Mapped[datetime]