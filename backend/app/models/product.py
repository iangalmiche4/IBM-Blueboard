"""
Product model
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    """Product model for cosmetics catalog"""

    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    brand = Column(String(100), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sales = relationship("Sale", back_populates="product")
    satisfaction_reviews = relationship("Satisfaction", back_populates="product")
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    returns = relationship("Return", back_populates="product")

    def __repr__(self):
        return f"<Product {self.name} ({self.sku})>"
