"""
Sales service - Business logic for sales operations
"""

from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models import Product, Sale
from app.schemas.sales import (
    RegionSale,
    SaleItem,
    SalesByRegion,
    SalesStats,
    TopProduct,
    TopProducts,
)


class SalesService:
    """Service for sales operations"""

    @staticmethod
    def get_sales(db: Session, skip: int = 0, limit: int = 100) -> List[SaleItem]:
        """
        Get all sales with product and customer information

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of SaleItem
        """
        sales = (
            db.query(Sale)
            .options(joinedload(Sale.product), joinedload(Sale.customer))
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [
            SaleItem(
                id=str(s.id),
                product_id=str(s.product_id),
                product_name=s.product.name if s.product else "Unknown Product",
                customer_id=str(s.customer_id),
                customer_name=(
                    f"{s.customer.first_name} {s.customer.last_name}"
                    if s.customer
                    else "Unknown Customer"
                ),
                quantity=s.quantity,
                unit_price=float(s.unit_price),
                total_amount=float(s.total_amount),
                sale_date=s.sale_date.isoformat(),
                region=s.region,
                channel=s.channel,
            )
            for s in sales
        ]

    @staticmethod
    def get_sales_stats(db: Session) -> SalesStats:
        """
        Get sales statistics

        Args:
            db: Database session

        Returns:
            SalesStats
        """
        total_revenue = db.query(func.sum(Sale.total_amount)).scalar() or 0
        total_sales = db.query(func.count(Sale.id)).scalar() or 0
        avg_basket = total_revenue / total_sales if total_sales > 0 else 0

        return SalesStats(
            total_revenue=float(total_revenue),
            total_sales=total_sales,
            average_basket=round(float(avg_basket), 2),
        )

    @staticmethod
    def get_sales_by_region(db: Session) -> SalesByRegion:
        """
        Get sales grouped by region

        Args:
            db: Database session

        Returns:
            SalesByRegion
        """
        results = (
            db.query(
                Sale.region,
                func.sum(Sale.total_amount).label("revenue"),
                func.count(Sale.id).label("count"),
            )
            .group_by(Sale.region)
            .all()
        )

        regions = [
            RegionSale(region=r.region, revenue=float(r.revenue), count=r.count)
            for r in results
        ]

        return SalesByRegion(regions=regions)

    @staticmethod
    def get_top_selling_products(db: Session, limit: int = 10) -> TopProducts:
        """
        Get top selling products

        Args:
            db: Database session
            limit: Maximum number of products to return

        Returns:
            TopProducts
        """
        results = (
            db.query(
                Product.name,
                func.sum(Sale.quantity).label("units_sold"),
                func.sum(Sale.total_amount).label("revenue"),
            )
            .join(Sale)
            .group_by(Product.id, Product.name)
            .order_by(func.sum(Sale.total_amount).desc())
            .limit(limit)
            .all()
        )

        products = [
            TopProduct(name=r.name, units_sold=r.units_sold, revenue=float(r.revenue))
            for r in results
        ]

        return TopProducts(products=products)
