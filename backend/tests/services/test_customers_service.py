"""
Tests for CustomersService
"""

from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.services.customers_service import CustomersService


class TestCustomersService:
    """Tests for CustomersService"""

    def test_get_all_customers(self, db_session, sample_customer):
        """Test getting all customers"""
        result = CustomersService.get_customers(db_session, skip=0, limit=10)

        assert len(result) == 1
        assert result[0].email == sample_customer.email

    def test_get_customers_with_segment_filter(self, db_session, sample_customer):
        """Test getting customers filtered by segment"""
        result = CustomersService.get_customers(
            db_session, skip=0, limit=10, segment=sample_customer.segment
        )

        assert len(result) >= 1
        assert all(c.segment == sample_customer.segment for c in result)

    def test_get_customer_by_id(self, db_session, sample_customer, sample_sale):
        """Test getting customer by ID with stats"""
        result = CustomersService.get_customer_by_id(db_session, sample_customer.id)

        assert result.id == str(sample_customer.id)
        assert result.email == sample_customer.email
        assert result.stats.total_orders >= 1
        assert result.stats.total_spent > 0

    def test_get_customer_by_id_not_found(self, db_session):
        """Test getting non-existent customer"""
        fake_id = uuid4()
        with pytest.raises(HTTPException) as exc_info:
            CustomersService.get_customer_by_id(db_session, fake_id)

        assert exc_info.value.status_code == 404

    def test_get_segment_distribution(self, db_session, sample_customer):
        """Test getting segment distribution"""
        result = CustomersService.get_segment_distribution(db_session)

        assert len(result.segments) > 0
        for segment in result.segments:
            assert segment.segment
            assert segment.count > 0
