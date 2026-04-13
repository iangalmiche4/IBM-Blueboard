"""
Products schemas - Pydantic models for products API
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base product schema"""

    id: str
    name: str
    category: str
    brand: str
    price: float = Field(..., gt=0)
    sku: str


class ProductDetail(ProductBase):
    """Detailed product schema with description"""

    description: Optional[str] = None


class ProductList(BaseModel):
    """List of products"""

    products: List[ProductBase]


class ProductsByCategory(BaseModel):
    """Products grouped by category"""

    category: str
    products: List[ProductBase]
    count: int
