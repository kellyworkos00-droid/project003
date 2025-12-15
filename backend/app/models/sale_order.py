from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db import Base


class SaleOrder(Base):
    __tablename__ = "sale_order"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    contact_id = Column(Integer, ForeignKey("contact.id"), nullable=True, index=True)
    status = Column(String(50), nullable=False, default="draft")  # draft, confirmed, shipped, invoiced
    total = Column(Numeric(12, 2), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    contact = relationship("Contact", backref="sale_orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("sale_order.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=True, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(12, 2), nullable=False, default=0)
    subtotal = Column(Numeric(12, 2), nullable=False, default=0)

    order = relationship("SaleOrder", back_populates="items")
    product = relationship("Product", backref="order_items")
