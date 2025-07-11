# backend/src/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create the SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL
    # The 'connect_args' is only needed for SQLite, not PostgreSQL
    # connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()


# --- Dependency for FastAPI ---
def get_db():
    """
    A dependency that provides a database session for each request.
    It ensures the session is always closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()