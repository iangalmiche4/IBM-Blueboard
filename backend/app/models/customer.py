"""
Customer model
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    """Customer model"""

    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    gender = Column(String(20))
    segment = Column(String(50), nullable=False, index=True)
    region = Column(String(100), nullable=False, index=True)
    registration_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sales = relationship("Sale", back_populates="customer")
    satisfaction_reviews = relationship("Satisfaction", back_populates="customer")
    returns = relationship("Return", back_populates="customer")

    def __repr__(self):
        return f"<Customer {self.first_name} {self.last_name} ({self.email})>"
