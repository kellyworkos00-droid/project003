from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, func, Date
from sqlalchemy.orm import relationship
from app.db import Base


class Invoice(Base):
    __tablename__ = "invoice"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    sale_order_id = Column(Integer, ForeignKey("sale_order.id"), nullable=True, index=True)
    contact_id = Column(Integer, ForeignKey("contact.id"), nullable=True, index=True)
    status = Column(String(50), nullable=False, default="draft")  # draft, sent, paid, cancelled
    invoice_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    subtotal = Column(Numeric(12, 2), nullable=False, default=0)
    tax = Column(Numeric(12, 2), nullable=False, default=0)
    total = Column(Numeric(12, 2), nullable=False, default=0)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    sale_order = relationship("SaleOrder", backref="invoices")
    contact = relationship("Contact", backref="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    __tablename__ = "invoice_item"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoice.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=True, index=True)
    description = Column(String(200), nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(12, 2), nullable=False, default=0)
    subtotal = Column(Numeric(12, 2), nullable=False, default=0)

    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product", backref="invoice_items")
