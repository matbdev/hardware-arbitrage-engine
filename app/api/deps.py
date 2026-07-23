from typing import Generator
from sqlalchemy.orm import Session, sessionmaker
from app.config import db_engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

def get_db() -> Generator[Session, None, None]:
    """
    Injects a database session on the route and guarantee
    the automatically clousure at the end
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()