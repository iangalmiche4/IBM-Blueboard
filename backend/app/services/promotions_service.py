"""
Promotions service - Business logic for promotions management
"""

from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.promotion import Promotion
from app.models.sale import Sale
from app.schemas.promotions import PromotionROI, PromotionStats, PromotionWithSale


class PromotionsService:
    """Service for promotions operations"""

    @staticmethod
    def get_all_promotions(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[Promotion]:
        """Get all promotions"""
        return db.query(Promotion).offset(skip).limit(limit).all()

    @staticmethod
    def get_promotion_by_id(db: Session, promotion_id: UUID) -> Optional[Promotion]:
        """Get promotion by ID"""
        return db.query(Promotion).filter(Promotion.id == promotion_id).first()

    @staticmethod
    def get_promotions_with_sales(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[PromotionWithSale]:
        """Get promotions with sale details"""
        results = (
            db.query(
                Promotion,
                Sale.total_amount.label("sale_total_amount"),
                (Customer.first_name + " " + Customer.last_name).label("customer_name"),
            )
            .join(Sale, Promotion.sale_id == Sale.id)
            .join(Customer, Sale.customer_id == Customer.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [
            PromotionWithSale(
                id=promo.id,
                sale_id=promo.sale_id,
                promo_code=promo.promo_code,
                promo_type=promo.promo_type,
                discount_percentage=promo.discount_percentage,
                start_date=promo.start_date,
                end_date=promo.end_date,
                created_at=promo.created_at,
                sale_total_amount=sale_total_amount,
                customer_name=customer_name,
            )
            for promo, sale_total_amount, customer_name in results
        ]

    @staticmethod
    def get_active_promotions(
        db: Session, current_date: date = None
    ) -> List[Promotion]:
        """Get currently active promotions"""
        if current_date is None:
            current_date = date.today()

        return (
            db.query(Promotion)
            .filter(Promotion.start_date <= current_date)
            .filter(Promotion.end_date >= current_date)
            .all()
        )

    @staticmethod
    def get_promotions_by_type(db: Session, promo_type: str) -> List[Promotion]:
        """Get promotions by type"""
        return db.query(Promotion).filter(Promotion.promo_type == promo_type).all()

    @staticmethod
    def get_promotion_stats(db: Session) -> PromotionStats:
        """Get promotion statistics"""
        # Total promotions
        total_promotions = db.query(func.count(Promotion.id)).scalar() or 0

        # Active promotions
        current_date = date.today()
        active_promotions = (
            db.query(func.count(Promotion.id))
            .filter(Promotion.start_date <= current_date)
            .filter(Promotion.end_date >= current_date)
            .scalar()
            or 0
        )

        # Total discount given (discount_percentage * sale_total_amount / 100)
        total_discount_given = (
            db.query(func.sum(Sale.total_amount * Promotion.discount_percentage / 100))
            .select_from(Promotion)
            .join(Sale, Promotion.sale_id == Sale.id)
            .scalar()
            or 0.0
        )

        # Average discount percentage
        average_discount = (
            db.query(func.avg(Promotion.discount_percentage)).scalar() or 0.0
        )

        # Most used promo type
        most_used_result = (
            db.query(Promotion.promo_type, func.count(Promotion.id).label("count"))
            .group_by(Promotion.promo_type)
            .order_by(func.count(Promotion.id).desc())
            .first()
        )

        most_used_promo_type = most_used_result[0] if most_used_result else "N/A"

        # Promotion usage rate (sales with promotions / total sales as decimal)
        total_sales = db.query(func.count(Sale.id)).scalar() or 1
        sales_with_promos = (
            db.query(func.count(func.distinct(Promotion.sale_id))).scalar() or 0
        )
        promotion_usage_rate = (
            (sales_with_promos / total_sales) if total_sales > 0 else 0.0
        )

        # Total usage (number of times promotions were used)
        total_usage = db.query(func.count(Promotion.id)).scalar() or 0

        # Total revenue from promotional sales
        total_revenue = (
            db.query(func.sum(Sale.total_amount))
            .select_from(Promotion)
            .join(Sale, Promotion.sale_id == Sale.id)
            .scalar()
            or 0.0
        )

        # Average revenue per promotion
        average_revenue_per_promotion = (
            (total_revenue / total_promotions) if total_promotions > 0 else 0.0
        )

        return PromotionStats(
            total_promotions=total_promotions,
            active_promotions=active_promotions,
            total_discount_given=float(total_discount_given),
            average_discount=float(average_discount),
            most_used_promo_type=most_used_promo_type,
            promotion_usage_rate=float(promotion_usage_rate),
            total_usage=total_usage,
            total_revenue=float(total_revenue),
            average_revenue_per_promotion=float(average_revenue_per_promotion),
        )

    @staticmethod
    def get_promotion_roi(db: Session) -> List[PromotionROI]:
        """Get top performing promotions by revenue"""
        results = (
            db.query(
                Promotion.id,
                Promotion.promo_code,
                Promotion.promo_type,
                func.count(Sale.id).label("usage_count"),
                func.sum(Sale.total_amount).label("total_revenue"),
                func.sum(Sale.total_amount * Promotion.discount_percentage / 100).label(
                    "total_discount"
                ),
            )
            .select_from(Promotion)
            .join(Sale, Promotion.sale_id == Sale.id)
            .group_by(Promotion.id, Promotion.promo_code, Promotion.promo_type)
            .order_by(func.sum(Sale.total_amount).desc())
            .limit(10)
            .all()
        )

        return [
            PromotionROI(
                id=promo_id,
                promo_code=promo_code or "N/A",  # Handle None case
                promo_type=promo_type or "Unknown",  # Handle None case
                usage_count=usage_count,
                total_revenue=float(total_revenue or 0),
                total_discount=float(total_discount or 0),
                average_revenue_per_use=float(
                    total_revenue / usage_count if usage_count > 0 else 0
                ),
                roi_percentage=float(
                    ((total_revenue - total_discount) / total_discount * 100)
                    if total_discount and total_discount > 0
                    else 0
                ),
            )
            for promo_id, promo_code, promo_type, usage_count, total_revenue, total_discount in results
        ]
