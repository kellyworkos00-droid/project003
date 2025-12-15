from sqlalchemy import String, Integer, DateTime, func, Column
from app.db import Base


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    email = Column(String(320), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    company = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
