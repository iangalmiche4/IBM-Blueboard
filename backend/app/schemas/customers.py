"""
Customers schemas - Pydantic models for customers API
"""

from typing import List

from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    """Base customer schema"""

    id: str
    email: EmailStr
    first_name: str
    last_name: str
    segment: str
    region: str
    registration_date: str
    is_active: bool


class CustomerStats(BaseModel):
    """Customer purchase statistics"""

    total_spent: float
    total_orders: int


class CustomerDetail(CustomerBase):
    """Detailed customer with stats"""

    stats: CustomerStats


class CustomersList(BaseModel):
    """List of customers"""

    customers: List[CustomerBase]


class SegmentItem(BaseModel):
    """Customer segment distribution"""

    segment: str
    count: int


class SegmentDistribution(BaseModel):
    """Segments distribution"""

    segments: List[SegmentItem]
