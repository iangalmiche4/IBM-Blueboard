"""
Customers router
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.api import DEFAULT_LIMIT, DEFAULT_SKIP, MAX_LIMIT, MIN_LIMIT
from app.database import get_db
from app.schemas.customers import CustomerBase, CustomerDetail, SegmentDistribution
from app.services.customers_service import CustomersService

router = APIRouter()


@router.get("/", response_model=List[CustomerBase])
async def get_customers(
    skip: int = Query(DEFAULT_SKIP, ge=0),
    limit: int = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    segment: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get all customers with optional filtering"""
    return CustomersService.get_customers(db, skip, limit, segment)


@router.get("/{customer_id}", response_model=CustomerDetail)
async def get_customer(customer_id: UUID, db: Session = Depends(get_db)):
    """Get a specific customer by ID"""
    return CustomersService.get_customer_by_id(db, customer_id)


@router.get("/segments/distribution", response_model=SegmentDistribution)
async def get_segment_distribution(db: Session = Depends(get_db)):
    """Get customer distribution by segment"""
    return CustomersService.get_segment_distribution(db)
