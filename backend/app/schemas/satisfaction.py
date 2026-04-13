"""
Satisfaction schemas - Pydantic models for satisfaction/reviews API
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    """Base review schema"""

    id: str
    product_id: str
    customer_id: str
    overall_rating: int = Field(..., ge=1, le=5)
    quality_rating: int = Field(..., ge=1, le=5)
    price_rating: int = Field(..., ge=1, le=5)
    packaging_rating: int = Field(..., ge=1, le=5)
    delivery_rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    review_date: str
    verified_purchase: bool


class ReviewsList(BaseModel):
    """List of reviews"""

    reviews: List[ReviewBase]


class AverageRatings(BaseModel):
    """Average ratings by criteria"""

    overall: float = Field(..., ge=0, le=5)
    quality: float = Field(..., ge=0, le=5)
    price: float = Field(..., ge=0, le=5)
    packaging: float = Field(..., ge=0, le=5)
    delivery: float = Field(..., ge=0, le=5)


class SatisfactionStats(BaseModel):
    """Satisfaction statistics"""

    average_ratings: AverageRatings
    total_reviews: int


class ReviewSummary(BaseModel):
    """Review summary for display"""

    id: str
    overall_rating: int
    comment: Optional[str]
    review_date: str


class ProductReviews(BaseModel):
    """Reviews for a specific product"""

    product_id: str
    average_rating: float
    reviews: List[ReviewSummary]
    count: int


class AverageSatisfaction(BaseModel):
    """Overall average satisfaction"""

    average_rating: float
    total_reviews: int
