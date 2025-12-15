from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLite needs check_same_thread=False for use in FastAPI dev
connect_args = {"check_same_thread": False} if settings.sqlalchemy_database_uri.startswith("sqlite") else {}
engine = create_engine(settings.sqlalchemy_database_uri, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
