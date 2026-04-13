"""
Sales schemas - Pydantic models for sales API
"""

from typing import List

from pydantic import BaseModel, Field


class SaleItem(BaseModel):
    """Individual sale item"""

    id: str
    product_id: str
    product_name: str
    customer_id: str
    customer_name: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    total_amount: float = Field(..., gt=0)
    sale_date: str
    region: str
    channel: str


class SalesList(BaseModel):
    """List of sales"""

    sales: List[SaleItem]


class SalesStats(BaseModel):
    """Sales statistics"""

    total_revenue: float
    total_sales: int
    average_basket: float


class RegionSale(BaseModel):
    """Sales by region"""

    region: str
    revenue: float
    count: int


class SalesByRegion(BaseModel):
    """Sales grouped by region"""

    regions: List[RegionSale]


class TopProduct(BaseModel):
    """Top selling product"""

    name: str
    units_sold: int
    revenue: float


class TopProducts(BaseModel):
    """Top selling products"""

    products: List[TopProduct]
