"""
Inventory schemas for request/response validation
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class InventoryBase(BaseModel):
    """Base inventory schema"""

    product_id: UUID
    stock_quantity: int = Field(..., ge=0)
    reserved_quantity: int = Field(default=0, ge=0)
    warehouse_location: str = Field(..., max_length=100)
    last_restock_date: Optional[date] = None
    reorder_level: int = Field(..., ge=0)


class InventoryCreate(InventoryBase):
    """Schema for creating inventory"""


class InventoryUpdate(BaseModel):
    """Schema for updating inventory"""

    stock_quantity: Optional[int] = Field(None, ge=0)
    reserved_quantity: Optional[int] = Field(None, ge=0)
    warehouse_location: Optional[str] = Field(None, max_length=100)
    last_restock_date: Optional[date] = None
    reorder_level: Optional[int] = Field(None, ge=0)


class InventoryResponse(InventoryBase):
    """Schema for inventory response"""

    id: UUID
    updated_at: datetime

    class Config:
        from_attributes = True


class InventoryWithProduct(InventoryResponse):
    """Schema for inventory with product details"""

    product_name: str
    product_category: str
    product_sku: str


class LowStockAlert(BaseModel):
    """Schema for low stock alerts"""

    product_id: UUID
    product_name: str
    product_sku: str
    stock_quantity: int
    reorder_level: int
    warehouse_location: str
    shortage: int


class InventoryStats(BaseModel):
    """Schema for inventory statistics"""

    total_products: int
    total_stock_value: float
    low_stock_items: int
    out_of_stock_items: int
    total_reserved: int
    warehouses_count: int
