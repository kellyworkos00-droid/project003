from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)  # e.g., "contacts.read", "deals.write"
    description = Column(String(200), nullable=True)


class RolePermission(Base):
    __tablename__ = "role_permission"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_id = Column(Integer, ForeignKey("permission.id", ondelete="CASCADE"), nullable=False, index=True)
