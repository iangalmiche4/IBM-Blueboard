"""
Returns router - API endpoints for returns management
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config.api import DEFAULT_LIMIT, DEFAULT_SKIP, MAX_LIMIT, MIN_LIMIT
from app.database import get_db
from app.schemas.returns import (
    ProductReturnRate,
    ReturnReasonAnalysis,
    ReturnResponse,
    ReturnStats,
    ReturnWithDetails,
)
from app.services.returns_service import ReturnsService

router = APIRouter()


@router.get("/", response_model=List[ReturnResponse])
def get_returns(
    skip: int = Query(DEFAULT_SKIP, ge=0),
    limit: int = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    db: Session = Depends(get_db),
):
    """Get all returns"""
    return ReturnsService.get_all_returns(db, skip=skip, limit=limit)


@router.get("/with-details", response_model=List[ReturnWithDetails])
def get_returns_with_details(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get returns with product and customer details"""
    return ReturnsService.get_returns_with_details(db, skip=skip, limit=limit)


@router.get("/stats", response_model=ReturnStats)
def get_return_stats(db: Session = Depends(get_db)):
    """Get return statistics"""
    return ReturnsService.get_return_stats(db)


@router.get("/reason-analysis", response_model=List[ReturnReasonAnalysis])
def get_return_reason_analysis(db: Session = Depends(get_db)):
    """Get analysis of return reasons"""
    return ReturnsService.get_return_reason_analysis(db)


@router.get("/product-rates", response_model=List[ProductReturnRate])
def get_product_return_rates(limit: int = 10, db: Session = Depends(get_db)):
    """Get products with highest return rates"""
    return ReturnsService.get_product_return_rates(db, limit=limit)


@router.get("/status/{status}", response_model=List[ReturnResponse])
def get_returns_by_status(status: str, db: Session = Depends(get_db)):
    """Get returns by status"""
    return ReturnsService.get_returns_by_status(db, status)


@router.get("/customer/{customer_id}", response_model=List[ReturnResponse])
def get_returns_by_customer(customer_id: UUID, db: Session = Depends(get_db)):
    """Get returns by customer"""
    return ReturnsService.get_returns_by_customer(db, customer_id)


@router.get("/product/{product_id}", response_model=List[ReturnResponse])
def get_returns_by_product(product_id: UUID, db: Session = Depends(get_db)):
    """Get returns by product"""
    return ReturnsService.get_returns_by_product(db, product_id)


@router.get("/{return_id}", response_model=ReturnResponse)
def get_return_by_id(return_id: UUID, db: Session = Depends(get_db)):
    """Get return by ID"""
    return_item = ReturnsService.get_return_by_id(db, return_id)
    if not return_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Return not found"
        )
    return return_item
