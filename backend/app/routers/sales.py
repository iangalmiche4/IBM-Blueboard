"""
Sales router
"""

from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.api import DEFAULT_LIMIT, DEFAULT_SKIP, MAX_LIMIT, MIN_LIMIT
from app.database import get_db
from app.schemas.sales import SaleItem, SalesByRegion, SalesStats, TopProducts
from app.services.sales_service import SalesService

router = APIRouter()


@router.get("/", response_model=List[SaleItem])
async def get_sales(
    skip: int = Query(DEFAULT_SKIP, ge=0),
    limit: int = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    db: Session = Depends(get_db),
):
    """Get all sales with product and customer names"""
    return SalesService.get_sales(db, skip, limit)


@router.get("/stats", response_model=SalesStats)
async def get_sales_stats(db: Session = Depends(get_db)):
    """Get sales statistics"""
    return SalesService.get_sales_stats(db)


@router.get("/by-region", response_model=SalesByRegion)
async def get_sales_by_region(db: Session = Depends(get_db)):
    """Get sales grouped by region"""
    return SalesService.get_sales_by_region(db)


@router.get("/top-products", response_model=TopProducts)
async def get_top_selling_products(
    limit: int = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    db: Session = Depends(get_db),
):
    """Get top selling products"""
    return SalesService.get_top_selling_products(db, limit)
