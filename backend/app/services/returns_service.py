"""
Returns service - Business logic for returns management
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.product import Product
from app.models.return_model import Return
from app.models.sale import Sale
from app.schemas.returns import (
    ProductReturnRate,
    ReturnReasonAnalysis,
    ReturnStats,
    ReturnWithDetails,
)


class ReturnsService:
    """Service for returns operations"""

    @staticmethod
    def get_all_returns(db: Session, skip: int = 0, limit: int = 100) -> List[Return]:
        """Get all returns"""
        return db.query(Return).offset(skip).limit(limit).all()

    @staticmethod
    def get_return_by_id(db: Session, return_id: UUID) -> Optional[Return]:
        """Get return by ID"""
        return db.query(Return).filter(Return.id == return_id).first()

    @staticmethod
    def get_returns_with_details(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[ReturnWithDetails]:
        """Get returns with product and customer details"""
        results = (
            db.query(
                Return,
                Product.name.label("product_name"),
                Product.category.label("product_category"),
                (Customer.first_name + " " + Customer.last_name).label("customer_name"),
                Customer.email.label("customer_email"),
            )
            .join(Product, Return.product_id == Product.id)
            .join(Customer, Return.customer_id == Customer.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [
            ReturnWithDetails(
                id=ret.id,
                product_id=ret.product_id,
                customer_id=ret.customer_id,
                sale_id=ret.sale_id,
                quantity=ret.quantity,
                reason=ret.reason,
                status=ret.status,
                return_date=ret.return_date,
                refund_amount=ret.refund_amount,
                notes=ret.notes,
                created_at=ret.created_at,
                product_name=product_name,
                product_category=product_category,
                customer_name=customer_name,
                customer_email=customer_email,
            )
            for ret, product_name, product_category, customer_name, customer_email in results
        ]

    @staticmethod
    def get_returns_by_status(db: Session, status: str) -> List[Return]:
        """Get returns by status"""
        return db.query(Return).filter(Return.status == status).all()

    @staticmethod
    def get_returns_by_customer(db: Session, customer_id: UUID) -> List[Return]:
        """Get returns by customer"""
        return db.query(Return).filter(Return.customer_id == customer_id).all()

    @staticmethod
    def get_returns_by_product(db: Session, product_id: UUID) -> List[Return]:
        """Get returns by product"""
        return db.query(Return).filter(Return.product_id == product_id).all()

    @staticmethod
    def get_return_stats(db: Session) -> ReturnStats:
        """Get return statistics"""
        # Total returns
        total_returns = db.query(func.count(Return.id)).scalar() or 0

        # Total refund amount
        total_refund_amount = db.query(func.sum(Return.refund_amount)).scalar() or 0.0

        # Return rate (total returns / total sales as decimal, e.g., 0.06 for 6%)
        total_sales = db.query(func.count(Sale.id)).scalar() or 1
        return_rate = (total_returns / total_sales) if total_sales > 0 else 0.0

        # Average refund
        average_refund = db.query(func.avg(Return.refund_amount)).scalar() or 0.0

        # Pending returns
        pending_returns = (
            db.query(func.count(Return.id)).filter(Return.status == "Pending").scalar()
            or 0
        )

        # Approved returns
        approved_returns = (
            db.query(func.count(Return.id)).filter(Return.status == "Approved").scalar()
            or 0
        )

        return ReturnStats(
            total_returns=total_returns,
            total_refund_amount=float(total_refund_amount),
            return_rate=float(return_rate),
            average_refund_amount=float(average_refund),
            pending_returns=pending_returns,
            approved_returns=approved_returns,
        )

    @staticmethod
    def get_return_reason_analysis(db: Session) -> List[ReturnReasonAnalysis]:
        """Get analysis of return reasons"""
        total_returns = db.query(func.count(Return.id)).scalar() or 1

        results = (
            db.query(
                Return.reason,
                func.count(Return.id).label("count"),
                func.sum(Return.refund_amount).label("total_refund"),
            )
            .group_by(Return.reason)
            .order_by(func.count(Return.id).desc())
            .all()
        )

        return [
            ReturnReasonAnalysis(
                reason=reason,
                count=count,
                percentage=float(count / total_returns),
                total_refund_amount=float(total_refund or 0),
            )
            for reason, count, total_refund in results
        ]

    @staticmethod
    def get_product_return_rates(
        db: Session, limit: int = 10
    ) -> List[ProductReturnRate]:
        """Get products with highest return rates"""
        # Get total sold per product
        sales_per_product = (
            db.query(Sale.product_id, func.sum(Sale.quantity).label("total_sold"))
            .group_by(Sale.product_id)
            .subquery()
        )

        # Get total returned per product
        returns_per_product = (
            db.query(
                Return.product_id,
                func.sum(Return.quantity).label("total_returned"),
                func.sum(Return.refund_amount).label("total_refund"),
            )
            .group_by(Return.product_id)
            .subquery()
        )

        # Join and calculate return rate
        results = (
            db.query(
                Product.id,
                Product.name,
                Product.category,
                sales_per_product.c.total_sold,
                returns_per_product.c.total_returned,
                returns_per_product.c.total_refund,
            )
            .join(sales_per_product, Product.id == sales_per_product.c.product_id)
            .join(returns_per_product, Product.id == returns_per_product.c.product_id)
            .order_by(
                (
                    returns_per_product.c.total_returned
                    / sales_per_product.c.total_sold
                ).desc()
            )
            .limit(limit)
            .all()
        )

        return [
            ProductReturnRate(
                product_id=product_id,
                product_name=name,
                product_category=category,
                total_sold=int(total_sold or 0),
                total_returned=int(total_returned or 0),
                return_rate=float(
                    (total_returned / total_sold) if total_sold > 0 else 0
                ),
                total_refund=float(total_refund or 0),
            )
            for product_id, name, category, total_sold, total_returned, total_refund in results
        ]
