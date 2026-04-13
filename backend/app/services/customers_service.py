"""
Customers service - Business logic for customers operations
"""

from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Customer, Sale
from app.schemas.customers import (
    CustomerBase,
    CustomerDetail,
    CustomerStats,
    SegmentDistribution,
    SegmentItem,
)


class CustomersService:
    """Service for customers operations"""

    @staticmethod
    def get_customers(
        db: Session, skip: int = 0, limit: int = 100, segment: Optional[str] = None
    ) -> List[CustomerBase]:
        """
        Get all customers with optional segment filtering

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            segment: Optional segment filter

        Returns:
            List of CustomerBase
        """
        query = db.query(Customer)

        if segment:
            query = query.filter(Customer.segment == segment)

        customers = query.offset(skip).limit(limit).all()

        return [
            CustomerBase(
                id=str(c.id),
                email=c.email,
                first_name=c.first_name,
                last_name=c.last_name,
                segment=c.segment,
                region=c.region,
                registration_date=c.registration_date.isoformat(),
                is_active=c.is_active,
            )
            for c in customers
        ]

    @staticmethod
    def get_customer_by_id(db: Session, customer_id: UUID) -> CustomerDetail:
        """
        Get a specific customer by ID with purchase statistics

        Args:
            db: Database session
            customer_id: Customer UUID

        Returns:
            CustomerDetail

        Raises:
            HTTPException: If customer not found
        """
        customer = db.query(Customer).filter(Customer.id == customer_id).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Get customer's purchase history
        total_spent = (
            db.query(func.sum(Sale.total_amount))
            .filter(Sale.customer_id == customer_id)
            .scalar()
            or 0
        )

        total_orders = (
            db.query(func.count(Sale.id))
            .filter(Sale.customer_id == customer_id)
            .scalar()
            or 0
        )

        stats = CustomerStats(total_spent=float(total_spent), total_orders=total_orders)

        return CustomerDetail(
            id=str(customer.id),
            email=customer.email,
            first_name=customer.first_name,
            last_name=customer.last_name,
            segment=customer.segment,
            region=customer.region,
            registration_date=customer.registration_date.isoformat(),
            is_active=customer.is_active,
            stats=stats,
        )

    @staticmethod
    def get_segment_distribution(db: Session) -> SegmentDistribution:
        """
        Get customer distribution by segment

        Args:
            db: Database session

        Returns:
            SegmentDistribution
        """
        results = (
            db.query(Customer.segment, func.count(Customer.id).label("count"))
            .group_by(Customer.segment)
            .all()
        )

        segments = [SegmentItem(segment=r.segment, count=r.count) for r in results]

        return SegmentDistribution(segments=segments)
