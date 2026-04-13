"""
Promotion model
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Promotion(Base):
    """Promotion and discount model"""

    __tablename__ = "promotions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sale_id = Column(
        UUID(as_uuid=True), ForeignKey("sales.id"), nullable=False, index=True
    )
    promo_code = Column(String(50))
    promo_type = Column(String(50), nullable=False, index=True)
    discount_percentage = Column(Numeric(5, 2))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sale = relationship("Sale", back_populates="promotions")

    def __repr__(self):
        return f"<Promotion {self.promo_type} - {self.discount_percentage}%>"
