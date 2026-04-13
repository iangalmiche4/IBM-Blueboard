"""
Sale model
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Sale(Base):
    """Sale transaction model"""

    __tablename__ = "sales"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False, index=True
    )
    customer_id = Column(
        UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False, index=True
    )
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0)
    sale_date = Column(Date, nullable=False, index=True)
    region = Column(String(100), nullable=False, index=True)
    channel = Column(String(50), nullable=False, index=True)
    payment_method = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    promotions = relationship("Promotion", back_populates="sale")

    def __repr__(self):
        return f"<Sale {self.id} - {self.total_amount}€>"
