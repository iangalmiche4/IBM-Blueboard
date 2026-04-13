"""
Inventory router - API endpoints for inventory management
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config.api import DEFAULT_LIMIT, DEFAULT_SKIP, MAX_LIMIT, MIN_LIMIT
from app.database import get_db
from app.schemas.inventory import (
    InventoryResponse,
    InventoryStats,
    InventoryWithProduct,
    LowStockAlert,
)
from app.services.inventory_service import InventoryService

router = APIRouter()


@router.get("/", response_model=List[InventoryResponse])
def get_inventory(
    skip: int = Query(DEFAULT_SKIP, ge=0),
    limit: int = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    db: Session = Depends(get_db),
):
    """Get all inventory items"""
    return InventoryService.get_all_inventory(db, skip=skip, limit=limit)


@router.get("/with-products", response_model=List[InventoryWithProduct])
def get_inventory_with_products(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get inventory with product details"""
    return InventoryService.get_inventory_with_products(db, skip=skip, limit=limit)


@router.get("/low-stock", response_model=List[LowStockAlert])
def get_low_stock_alerts(db: Session = Depends(get_db)):
    """Get products with stock below reorder level"""
    return InventoryService.get_low_stock_alerts(db)


@router.get("/stats", response_model=InventoryStats)
def get_inventory_stats(db: Session = Depends(get_db)):
    """Get inventory statistics"""
    return InventoryService.get_inventory_stats(db)


@router.get("/warehouse/{warehouse}", response_model=List[InventoryResponse])
def get_inventory_by_warehouse(warehouse: str, db: Session = Depends(get_db)):
    """Get inventory by warehouse location"""
    return InventoryService.get_inventory_by_warehouse(db, warehouse)


@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory_by_id(inventory_id: UUID, db: Session = Depends(get_db)):
    """Get inventory by ID"""
    inventory = InventoryService.get_inventory_by_id(db, inventory_id)
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found"
        )
    return inventory


@router.get("/product/{product_id}", response_model=InventoryResponse)
def get_inventory_by_product(product_id: UUID, db: Session = Depends(get_db)):
    """Get inventory by product ID"""
    inventory = InventoryService.get_inventory_by_product(db, product_id)
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found for this product",
        )
    return inventory
