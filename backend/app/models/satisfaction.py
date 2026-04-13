"""
Satisfaction (Customer Review) model
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Satisfaction(Base):
    """Customer satisfaction review model"""

    __tablename__ = "satisfaction"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False, index=True
    )
    customer_id = Column(
        UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False, index=True
    )
    overall_rating = Column(Integer, nullable=False)
    quality_rating = Column(Integer, nullable=False)
    price_rating = Column(Integer, nullable=False)
    packaging_rating = Column(Integer, nullable=False)
    delivery_rating = Column(Integer, nullable=False)
    comment = Column(Text)
    review_date = Column(Date, nullable=False, index=True)
    verified_purchase = Column(Boolean, default=False)
    helpful_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="satisfaction_reviews")
    customer = relationship("Customer", back_populates="satisfaction_reviews")

    def __repr__(self):
        return f"<Satisfaction {self.id} - Rating: {self.overall_rating}/5>"
