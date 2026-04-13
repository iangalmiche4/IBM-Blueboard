"""
Products router
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.api import DEFAULT_LIMIT, DEFAULT_SKIP, MAX_LIMIT, MIN_LIMIT
from app.database import get_db
from app.schemas.products import ProductBase, ProductDetail, ProductsByCategory
from app.services.products_service import ProductsService

router = APIRouter()


@router.get("/", response_model=List[ProductBase])
async def get_products(
    skip: int = Query(DEFAULT_SKIP, ge=0),
    limit: int = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get all products with optional filtering"""
    return ProductsService.get_products(db, skip, limit, category)


@router.get("/{product_id}", response_model=ProductDetail)
async def get_product(product_id: UUID, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    return ProductsService.get_product_by_id(db, product_id)


@router.get("/category/{category}", response_model=ProductsByCategory)
async def get_products_by_category(category: str, db: Session = Depends(get_db)):
    """Get products by category"""
    return ProductsService.get_products_by_category(db, category)
