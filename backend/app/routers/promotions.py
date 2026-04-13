"""
Promotions router - API endpoints for promotions management
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config.api import DEFAULT_LIMIT, DEFAULT_SKIP, MAX_LIMIT, MIN_LIMIT
from app.database import get_db
from app.schemas.promotions import (
    PromotionResponse,
    PromotionROI,
    PromotionStats,
    PromotionWithSale,
)
from app.services.promotions_service import PromotionsService

router = APIRouter()


@router.get("/", response_model=List[PromotionResponse])
def get_promotions(
    skip: int = Query(DEFAULT_SKIP, ge=0),
    limit: int = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    db: Session = Depends(get_db),
):
    """Get all promotions"""
    return PromotionsService.get_all_promotions(db, skip=skip, limit=limit)


@router.get("/with-sales", response_model=List[PromotionWithSale])
def get_promotions_with_sales(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get promotions with sale details"""
    return PromotionsService.get_promotions_with_sales(db, skip=skip, limit=limit)


@router.get("/active", response_model=List[PromotionResponse])
def get_active_promotions(db: Session = Depends(get_db)):
    """Get currently active promotions"""
    return PromotionsService.get_active_promotions(db)


@router.get("/stats", response_model=PromotionStats)
def get_promotion_stats(db: Session = Depends(get_db)):
    """Get promotion statistics"""
    return PromotionsService.get_promotion_stats(db)


@router.get("/roi", response_model=List[PromotionROI])
def get_promotion_roi(db: Session = Depends(get_db)):
    """Get ROI analysis by promotion type"""
    return PromotionsService.get_promotion_roi(db)


@router.get("/type/{promo_type}", response_model=List[PromotionResponse])
def get_promotions_by_type(promo_type: str, db: Session = Depends(get_db)):
    """Get promotions by type"""
    return PromotionsService.get_promotions_by_type(db, promo_type)


@router.get("/{promotion_id}", response_model=PromotionResponse)
def get_promotion_by_id(promotion_id: UUID, db: Session = Depends(get_db)):
    """Get promotion by ID"""
    promotion = PromotionsService.get_promotion_by_id(db, promotion_id)
    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found"
        )
    return promotion
