"""
Satisfaction (Reviews) router
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.api import DEFAULT_LIMIT, DEFAULT_SKIP, MAX_LIMIT, MIN_LIMIT
from app.database import get_db
from app.schemas.satisfaction import (
    AverageSatisfaction,
    ProductReviews,
    ReviewBase,
    SatisfactionStats,
)
from app.services.satisfaction_service import SatisfactionService

router = APIRouter()


@router.get("/", response_model=List[ReviewBase])
async def get_reviews(
    skip: int = Query(DEFAULT_SKIP, ge=0),
    limit: int = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    db: Session = Depends(get_db),
):
    """Get all satisfaction reviews"""
    return SatisfactionService.get_reviews(db, skip, limit)


@router.get("/stats", response_model=SatisfactionStats)
async def get_satisfaction_stats(db: Session = Depends(get_db)):
    """Get satisfaction statistics"""
    return SatisfactionService.get_satisfaction_stats(db)


@router.get("/by-product/{product_id}", response_model=ProductReviews)
async def get_product_reviews(product_id: UUID, db: Session = Depends(get_db)):
    """Get reviews for a specific product"""
    return SatisfactionService.get_product_reviews(db, product_id)


@router.get("/average", response_model=AverageSatisfaction)
async def get_average_satisfaction(db: Session = Depends(get_db)):
    """Get overall average satisfaction rating"""
    return SatisfactionService.get_average_satisfaction(db)
