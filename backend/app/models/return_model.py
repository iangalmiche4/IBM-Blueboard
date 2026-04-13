"""
Return model
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Return(Base):
    """Product return model"""

    __tablename__ = "returns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False, index=True
    )
    customer_id = Column(
        UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False, index=True
    )
    sale_id = Column(
        UUID(as_uuid=True), ForeignKey("sales.id"), nullable=False, index=True
    )
    quantity = Column(Integer, nullable=False)
    reason = Column(String(200), nullable=False)
    status = Column(String(50), nullable=False, index=True)
    return_date = Column(Date, nullable=False, index=True)
    refund_amount = Column(Numeric(10, 2), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="returns")
    customer = relationship("Customer", back_populates="returns")

    def __repr__(self):
        return f"<Return {self.id} - Status: {self.status}>"
