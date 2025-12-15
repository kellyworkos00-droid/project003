from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Deal(Base):
    __tablename__ = "deal"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False, default=0)
    stage = Column(String(50), nullable=True)
    contact_id = Column(Integer, ForeignKey("contact.id"), nullable=True, index=True)

    contact = relationship("Contact", backref="deals")
