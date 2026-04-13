"""
Returns schemas for request/response validation
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ReturnBase(BaseModel):
    """Base return schema"""

    product_id: UUID
    customer_id: UUID
    sale_id: UUID
    quantity: int = Field(..., ge=1)
    reason: str = Field(..., max_length=200)
    status: str = Field(..., max_length=50)
    return_date: date
    refund_amount: Decimal = Field(..., ge=0)
    notes: Optional[str] = None


class ReturnCreate(ReturnBase):
    """Schema for creating return"""


class ReturnUpdate(BaseModel):
    """Schema for updating return"""

    quantity: Optional[int] = Field(None, ge=1)
    reason: Optional[str] = Field(None, max_length=200)
    status: Optional[str] = Field(None, max_length=50)
    refund_amount: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None


class ReturnResponse(ReturnBase):
    """Schema for return response"""

    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ReturnWithDetails(ReturnResponse):
    """Schema for return with product and customer details"""

    product_name: str
    product_category: str
    customer_name: str
    customer_email: str


class ReturnStats(BaseModel):
    """Schema for return statistics"""

    total_returns: int
    total_refund_amount: float
    return_rate: float
    average_refund_amount: float
    pending_returns: int
    approved_returns: int


class ReturnReasonAnalysis(BaseModel):
    """Schema for return reason analysis"""

    reason: str
    count: int
    percentage: float
    total_refund_amount: float


class ProductReturnRate(BaseModel):
    """Schema for product return rate"""

    product_id: UUID
    product_name: str
    product_category: str
    total_sold: int
    total_returned: int
    return_rate: float
    total_refund: float
