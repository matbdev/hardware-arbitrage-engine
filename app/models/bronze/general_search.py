from datetime import datetime as dt
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class GeneralSearch(Base):
    """
    SQLAlchemy model representing the 'bronze_ad_links' table.
    Stores the raw advertisement links discovered during the initial scraping phase.
    """
    __tablename__ = "bronze_ad_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    subcategory: Mapped[str]
    item: Mapped[str]
    url: Mapped[str]
    status: Mapped[int]
    region: Mapped[str]
    link: Mapped[str]
    datetime: Mapped[dt] = mapped_column(default=dt.now)
    store: Mapped[str]
    available: Mapped[bool] = mapped_column(default=True)
