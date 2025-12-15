from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app.db import Base
import enum

class AccountType(str, enum.Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"

class Currency(Base):
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, index=True, nullable=False)  # e.g., USD, EUR
    name = Column(String(50), nullable=False)
    symbol = Column(String(10), nullable=True)

class ExchangeRate(Base):
    __tablename__ = "exchange_rate"
    id = Column(Integer, primary_key=True)
    base_currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False, index=True)
    quote_currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False, index=True)
    rate = Column(Numeric(18, 8), nullable=False)
    as_of = Column(DateTime(timezone=True), server_default=func.now())
    base_currency = relationship("Currency", foreign_keys=[base_currency_id])
    quote_currency = relationship("Currency", foreign_keys=[quote_currency_id])

class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(Enum(AccountType), nullable=False)
    parent_id = Column(Integer, ForeignKey("account.id"), nullable=True)
    currency_id = Column(Integer, ForeignKey("currency.id"), nullable=True)
    parent = relationship("Account", remote_side=[id])
    currency = relationship("Currency")

class JournalEntry(Base):
    __tablename__ = "journal_entry"
    id = Column(Integer, primary_key=True)
    ref = Column(String(100), nullable=True, index=True)
    memo = Column(String(200), nullable=True)
    currency_id = Column(Integer, ForeignKey("currency.id"), nullable=True)
    posted_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    currency = relationship("Currency")
    lines = relationship("JournalLine", back_populates="entry", cascade="all, delete-orphan")

class JournalLine(Base):
    __tablename__ = "journal_line"
    id = Column(Integer, primary_key=True)
    entry_id = Column(Integer, ForeignKey("journal_entry.id", ondelete="CASCADE"), index=True, nullable=False)
    account_id = Column(Integer, ForeignKey("account.id"), index=True, nullable=False)
    description = Column(String(200), nullable=True)
    debit = Column(Numeric(12, 2), nullable=False, default=0)
    credit = Column(Numeric(12, 2), nullable=False, default=0)
    entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("Account")
