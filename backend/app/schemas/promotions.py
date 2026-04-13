"""
Promotions schemas for request/response validation
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PromotionBase(BaseModel):
    """Base promotion schema"""

    sale_id: UUID
    promo_code: Optional[str] = Field(None, max_length=50)
    promo_type: str = Field(..., max_length=50)
    discount_percentage: Decimal = Field(..., ge=0, le=100)
    start_date: date
    end_date: date


class PromotionCreate(PromotionBase):
    """Schema for creating promotion"""


class PromotionUpdate(BaseModel):
    """Schema for updating promotion"""

    promo_code: Optional[str] = Field(None, max_length=50)
    promo_type: Optional[str] = Field(None, max_length=50)
    discount_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class PromotionResponse(PromotionBase):
    """Schema for promotion response"""

    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class PromotionWithSale(PromotionResponse):
    """Schema for promotion with sale details"""

    sale_total_amount: Decimal
    customer_name: str


class PromotionStats(BaseModel):
    """Schema for promotion statistics"""

    total_promotions: int
    active_promotions: int
    total_discount_given: float
    average_discount: float
    most_used_promo_type: str
    promotion_usage_rate: float
    total_usage: int
    total_revenue: float
    average_revenue_per_promotion: float


class PromotionROI(BaseModel):
    """Schema for top performing promotions"""

    id: UUID
    promo_code: str
    promo_type: str
    usage_count: int
    total_revenue: float
    total_discount: float
    average_revenue_per_use: float
    roi_percentage: float
