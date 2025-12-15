from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)  # admin, sales, viewer
    description = Column(String(200), nullable=True)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(320), unique=True, nullable=True, index=True)
    password_hash = Column(String(200), nullable=True)  # hashed password (bcrypt, etc.)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False, index=True)
    is_active = Column(Integer, nullable=False, default=1)  # SQLite uses integer for boolean
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    role = relationship("Role", backref="users")
