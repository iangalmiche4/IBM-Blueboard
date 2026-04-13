"""
Products service - Business logic for products operations
"""

from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Product
from app.schemas.products import ProductBase, ProductDetail, ProductsByCategory


class ProductsService:
    """Service for products operations"""

    @staticmethod
    def get_products(
        db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None
    ) -> List[ProductBase]:
        """
        Get all products with optional category filtering

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            category: Optional category filter

        Returns:
            List of ProductBase
        """
        query = db.query(Product)

        if category:
            query = query.filter(Product.category == category)

        products = query.offset(skip).limit(limit).all()

        return [
            ProductBase(
                id=str(p.id),
                name=p.name,
                category=p.category,
                brand=p.brand,
                price=float(p.price),
                sku=p.sku,
            )
            for p in products
        ]

    @staticmethod
    def get_product_by_id(db: Session, product_id: UUID) -> ProductDetail:
        """
        Get a specific product by ID

        Args:
            db: Database session
            product_id: Product UUID

        Returns:
            ProductDetail

        Raises:
            HTTPException: If product not found
        """
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return ProductDetail(
            id=str(product.id),
            name=product.name,
            category=product.category,
            brand=product.brand,
            price=float(product.price),
            sku=product.sku,
            description=product.description,
        )

    @staticmethod
    def get_products_by_category(db: Session, category: str) -> ProductsByCategory:
        """
        Get products grouped by category

        Args:
            db: Database session
            category: Category name

        Returns:
            ProductsByCategory
        """
        products = db.query(Product).filter(Product.category == category).all()

        product_list = [
            ProductBase(
                id=str(p.id),
                name=p.name,
                category=p.category,
                brand=p.brand,
                price=float(p.price),
                sku=p.sku,
            )
            for p in products
        ]

        return ProductsByCategory(
            category=category, products=product_list, count=len(product_list)
        )
