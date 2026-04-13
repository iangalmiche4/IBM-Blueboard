"""
Tests for AnalyticsService
"""

from datetime import date, datetime

from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale
from app.models.satisfaction import Satisfaction
from app.services.analytics_service import AnalyticsService


class TestAnalyticsService:
    """Tests for AnalyticsService"""

    def test_get_dashboard_data(self, db_session, sample_sale, sample_satisfaction):
        """Test getting dashboard data with KPIs"""
        result = AnalyticsService.get_dashboard_data(db_session)

        assert result.kpis.total_revenue > 0
        assert result.kpis.total_sales == 1
        assert result.kpis.avg_satisfaction > 0
        assert result.kpis.total_customers == 1
        assert result.kpis.avg_basket > 0
        assert isinstance(result.timestamp, datetime)

    def test_get_dashboard_data_empty_db(self, db_session):
        """Test dashboard data with empty database"""
        result = AnalyticsService.get_dashboard_data(db_session)

        assert result.kpis.total_revenue == 0
        assert result.kpis.total_sales == 0
        assert result.kpis.avg_satisfaction == 0
        assert result.kpis.total_customers == 0
        assert result.kpis.avg_basket == 0

    def test_get_sales_trends(self, db_session, multiple_sales):
        """Test getting sales trends by month"""
        result = AnalyticsService.get_sales_trends(db_session)

        assert len(result.trends) > 0
        for trend in result.trends:
            assert trend.revenue > 0
            assert trend.count > 0

    def test_get_top_products(self, db_session, multiple_sales):
        """Test getting top products by revenue"""
        result = AnalyticsService.get_top_products(db_session, limit=3)

        assert len(result.products) <= 3
        assert len(result.products) > 0

        # Check products are sorted by revenue (descending)
        revenues = [p.revenue for p in result.products]
        assert revenues == sorted(revenues, reverse=True)

    def test_get_category_distribution(self, db_session, multiple_sales):
        """Test getting category distribution"""
        result = AnalyticsService.get_category_distribution(db_session)

        assert len(result.distribution) > 0
        for category in result.distribution:
            assert category.category
            assert category.revenue > 0
            assert category.count > 0

    def test_get_kpi_trends(self, db_session):
        """Test getting KPI trends with historical comparison - covers calc_change with previous != 0"""
        from datetime import datetime, timedelta

        # Clean all existing data to ensure test isolation
        db_session.query(Satisfaction).delete()
        db_session.query(Sale).delete()
        db_session.query(Customer).delete()
        db_session.query(Product).delete()
        db_session.flush()  # Flush instead of commit - commit happens implicitly with add/refresh

        # Create dedicated product and customer for this test to avoid fixture pollution
        product = Product(
            name="KPI Test Product",
            category="Test",
            brand="Test Brand",
            price=50.0,
            sku="KPI-TEST-001",
            description="Product for KPI trends test",
        )
        db_session.add(product)

        customer = Customer(
            email="kpi_test@example.com",
            first_name="KPI",
            last_name="Test",
            birth_date=date(1990, 1, 1),
            gender="Male",
            segment="Standard",
            region="Europe",
            registration_date=date.today() - timedelta(days=365),
            is_active=True,
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(product)
        db_session.refresh(customer)

        # Create sales in previous period (60-30 days ago)
        previous_date = (datetime.utcnow() - timedelta(days=45)).date()
        sale_previous = Sale(
            product_id=product.id,
            customer_id=customer.id,
            quantity=1,
            unit_price=50.0,
            total_amount=50.0,
            sale_date=previous_date,
            channel="Online",
            region="Europe",
            payment_method="Credit Card",
        )
        db_session.add(sale_previous)

        # Create satisfaction in previous period
        satisfaction_previous = Satisfaction(
            product_id=product.id,
            customer_id=customer.id,
            overall_rating=4.0,
            quality_rating=4.0,
            price_rating=4.0,
            packaging_rating=4.0,
            delivery_rating=4.0,
            review_date=previous_date,
            comment="Previous period review",
        )
        db_session.add(satisfaction_previous)

        # Create sales in current period (last 30 days)
        current_date = (datetime.utcnow() - timedelta(days=15)).date()
        sale_current = Sale(
            product_id=product.id,
            customer_id=customer.id,
            quantity=2,
            unit_price=60.0,
            total_amount=120.0,
            sale_date=current_date,
            channel="Online",
            region="Europe",
            payment_method="Credit Card",
        )
        db_session.add(sale_current)

        # Create satisfaction in current period
        satisfaction_current = Satisfaction(
            product_id=product.id,
            customer_id=customer.id,
            overall_rating=5,  # Integer, not float
            quality_rating=5,
            price_rating=5,
            packaging_rating=5,
            delivery_rating=5,
            review_date=current_date,
            comment="Current period review",
        )
        db_session.add(satisfaction_current)
        db_session.commit()

        result = AnalyticsService.get_kpi_trends(db_session, period_days=30)

        assert result.period_days == 30
        # Current period should have higher revenue (120 vs 50)
        assert result.total_revenue.current == 120.0
        assert result.total_revenue.previous == 50.0
        assert result.total_revenue.change_percentage == 140.0  # (120-50)/50 * 100

        # Both periods have 1 sale each (count of Sale records, not quantity)
        assert result.total_sales.current == 1.0
        assert result.total_sales.previous == 1.0
        assert result.total_sales.change_percentage == 0.0  # (1-1)/1 * 100

        # Satisfaction should be higher in current period (5.0 vs 4.0)
        assert result.avg_satisfaction.current == 5.0
        assert result.avg_satisfaction.previous == 4.0
        assert result.avg_satisfaction.change_percentage == 25.0  # (5.0-4.0)/4.0 * 100

        # Avg basket should be higher (120 vs 50)
        assert result.avg_basket.current == 120.0
        assert result.avg_basket.previous == 50.0
        assert result.avg_basket.change_percentage == 140.0  # (120-50)/50 * 100

    def test_get_quick_stats(
        self, db_session, sample_product, sample_customer, multiple_sales
    ):
        """Test getting quick stats"""
        result = AnalyticsService.get_quick_stats(db_session)

        assert result.active_products >= 1
        assert result.active_customers >= 1
        assert result.avg_order_value >= 0
        assert 0 <= result.return_rate <= 1
