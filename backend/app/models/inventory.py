"""
Inventory model
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Inventory(Base):
    """Inventory tracking model"""

    __tablename__ = "inventory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        unique=True,
        nullable=False,
        index=True,
    )
    stock_quantity = Column(Integer, nullable=False)
    reserved_quantity = Column(Integer, default=0)
    warehouse_location = Column(String(100), nullable=False)
    last_restock_date = Column(Date)
    reorder_level = Column(Integer, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="inventory")

    def __repr__(self):
        return f"<Inventory {self.product_id} - Stock: {self.stock_quantity}>"
