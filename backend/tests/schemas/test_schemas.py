"""
Tests for Pydantic schemas validation
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.analytics import DashboardResponse, KPIData
from app.schemas.customers import CustomerBase
from app.schemas.products import ProductBase, ProductDetail


class TestAnalyticsSchemas:
    """Tests for analytics schemas"""

    def test_kpi_data_valid(self):
        """Test valid KPI data"""
        kpi = KPIData(
            total_revenue=10000.50,
            total_sales=100,
            avg_satisfaction=4.5,
            total_customers=50,
            avg_basket=100.00,
        )

        assert kpi.total_revenue == 10000.50
        assert kpi.avg_satisfaction == 4.5

    def test_kpi_data_satisfaction_range(self):
        """Test satisfaction rating must be between 0 and 5"""
        with pytest.raises(ValidationError):
            KPIData(
                total_revenue=10000,
                total_sales=100,
                avg_satisfaction=6.0,  # Invalid: > 5
                total_customers=50,
                avg_basket=100,
            )

    def test_dashboard_response(self):
        """Test dashboard response schema"""
        kpi = KPIData(
            total_revenue=10000,
            total_sales=100,
            avg_satisfaction=4.5,
            total_customers=50,
            avg_basket=100,
        )

        response = DashboardResponse(kpis=kpi, timestamp=datetime.now())

        assert response.kpis.total_revenue == 10000
        assert isinstance(response.timestamp, datetime)


class TestProductsSchemas:
    """Tests for products schemas"""

    def test_product_base_valid(self):
        """Test valid product base"""
        product = ProductBase(
            id="123e4567-e89b-12d3-a456-426614174000",
            name="Test Product",
            category="Skincare",
            brand="Test Brand",
            price=29.99,
            sku="TEST-001",
        )

        assert product.name == "Test Product"
        assert product.price == 29.99

    def test_product_detail(self):
        """Test product detail schema"""
        product = ProductDetail(
            id="123e4567-e89b-12d3-a456-426614174000",
            name="Test Product",
            category="Skincare",
            brand="Test Brand",
            price=29.99,
            sku="TEST-001",
            description="A great product",
        )

        assert product.description == "A great product"


class TestCustomersSchemas:
    """Tests for customers schemas"""

    def test_customer_base_valid_email(self):
        """Test customer with valid email"""
        customer = CustomerBase(
            id="123e4567-e89b-12d3-a456-426614174000",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            segment="Premium",
            region="Île-de-France",
            registration_date="2024-01-15",
            is_active=True,
        )

        assert customer.email == "test@example.com"
        assert customer.segment == "Premium"

    def test_customer_base_invalid_email(self):
        """Test customer with invalid email"""
        with pytest.raises(ValidationError):
            CustomerBase(
                id="123e4567-e89b-12d3-a456-426614174000",
                email="invalid-email",  # Invalid email format
                first_name="John",
                last_name="Doe",
                segment="Premium",
                region="Île-de-France",
                registration_date="2024-01-15",
                is_active=True,
            )


class TestSchemaValidation:
    """Tests for general schema validation"""

    def test_satisfaction_rating_constraints(self):
        """Test that satisfaction rating is constrained between 0 and 5"""
        # Valid rating
        kpi = KPIData(
            total_revenue=1000,
            total_sales=100,
            avg_satisfaction=4.5,
            total_customers=50,
            avg_basket=100,
        )
        assert kpi.avg_satisfaction == 4.5

        # Invalid rating > 5
        with pytest.raises(ValidationError):
            KPIData(
                total_revenue=1000,
                total_sales=100,
                avg_satisfaction=6.0,  # Should be rejected
                total_customers=50,
                avg_basket=100,
            )
