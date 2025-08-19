from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Numeric, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String, nullable=False)
    symbol = Column(String, nullable=True)
    isin = Column(String, nullable=True)
    exchange = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    business_unit = Column(String, nullable=True)
    geography = Column(String, nullable=True)
    order_value_inr = Column(Numeric(20, 2), nullable=True)
    currency_original = Column(String, nullable=True)
    original_value_text = Column(String, nullable=True)
    value_confidence = Column(String, nullable=True)
    client_name = Column(String, nullable=True)
    order_type = Column(String, nullable=True)
    duration_text = Column(String, nullable=True)
    announcement_time_ist = Column(DateTime(timezone=True), nullable=False)
    announcement_date_ist = Column(Date, nullable=True)
    materiality_flag = Column(Boolean, default=None)
    confidence_score = Column(Numeric(5, 4), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    sources = relationship("Source", back_populates="order")

class Source(Base):
    __tablename__ = "sources"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    source_type = Column(String, nullable=False)
    source_url = Column(Text, nullable=False)
    pdf_url = Column(Text, nullable=True)
    hash = Column(String, nullable=True)
    order = relationship("Order", back_populates="sources")
