"""
Satisfaction service - Business logic for satisfaction/reviews operations
"""

from typing import List
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Satisfaction
from app.schemas.satisfaction import (
    AverageRatings,
    AverageSatisfaction,
    ProductReviews,
    ReviewBase,
    ReviewSummary,
    SatisfactionStats,
)


class SatisfactionService:
    """Service for satisfaction/reviews operations"""

    @staticmethod
    def get_reviews(db: Session, skip: int = 0, limit: int = 100) -> List[ReviewBase]:
        """
        Get all satisfaction reviews

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of ReviewBase
        """
        reviews = db.query(Satisfaction).offset(skip).limit(limit).all()

        return [
            ReviewBase(
                id=str(r.id),
                product_id=str(r.product_id),
                customer_id=str(r.customer_id),
                overall_rating=r.overall_rating,
                quality_rating=r.quality_rating,
                price_rating=r.price_rating,
                packaging_rating=r.packaging_rating,
                delivery_rating=r.delivery_rating,
                comment=r.comment,
                review_date=r.review_date.isoformat(),
                verified_purchase=r.verified_purchase,
            )
            for r in reviews
        ]

    @staticmethod
    def get_satisfaction_stats(db: Session) -> SatisfactionStats:
        """
        Get satisfaction statistics

        Args:
            db: Database session

        Returns:
            SatisfactionStats
        """
        avg_ratings = db.query(
            func.avg(Satisfaction.overall_rating).label("overall"),
            func.avg(Satisfaction.quality_rating).label("quality"),
            func.avg(Satisfaction.price_rating).label("price"),
            func.avg(Satisfaction.packaging_rating).label("packaging"),
            func.avg(Satisfaction.delivery_rating).label("delivery"),
            func.count(Satisfaction.id).label("total_reviews"),
        ).first()

        ratings = AverageRatings(
            overall=round(float(avg_ratings.overall or 0), 2),
            quality=round(float(avg_ratings.quality or 0), 2),
            price=round(float(avg_ratings.price or 0), 2),
            packaging=round(float(avg_ratings.packaging or 0), 2),
            delivery=round(float(avg_ratings.delivery or 0), 2),
        )

        return SatisfactionStats(
            average_ratings=ratings, total_reviews=avg_ratings.total_reviews
        )

    @staticmethod
    def get_product_reviews(db: Session, product_id: UUID) -> ProductReviews:
        """
        Get reviews for a specific product

        Args:
            db: Database session
            product_id: Product UUID

        Returns:
            ProductReviews
        """
        reviews = (
            db.query(Satisfaction).filter(Satisfaction.product_id == product_id).all()
        )

        if not reviews:
            return ProductReviews(
                product_id=str(product_id), average_rating=0.0, reviews=[], count=0
            )

        avg_rating = sum(r.overall_rating for r in reviews) / len(reviews)

        review_summaries = [
            ReviewSummary(
                id=str(r.id),
                overall_rating=r.overall_rating,
                comment=r.comment,
                review_date=r.review_date.isoformat(),
            )
            for r in reviews
        ]

        return ProductReviews(
            product_id=str(product_id),
            average_rating=round(avg_rating, 2),
            reviews=review_summaries,
            count=len(reviews),
        )

    @staticmethod
    def get_average_satisfaction(db: Session) -> AverageSatisfaction:
        """
        Get overall average satisfaction rating

        Args:
            db: Database session

        Returns:
            AverageSatisfaction
        """
        avg_rating = db.query(func.avg(Satisfaction.overall_rating)).scalar() or 0
        total_reviews = db.query(func.count(Satisfaction.id)).scalar() or 0

        return AverageSatisfaction(
            average_rating=round(float(avg_rating), 2), total_reviews=total_reviews
        )
