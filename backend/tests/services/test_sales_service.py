"""
Tests for SalesService
"""

from app.services.products_service import ProductsService
from app.services.sales_service import SalesService


class TestSalesService:

    def test_get_products_by_category(self, db_session, multiple_products):
        """Test getting products filtered by category"""
        result = ProductsService.get_products(
            db_session, skip=0, limit=10, category="Skincare"
        )

        assert len(result) > 0
        assert all(p.category == "Skincare" for p in result)

    """Tests for SalesService"""

    def test_get_all_sales(self, db_session, multiple_sales):
        """Test getting all sales"""
        result = SalesService.get_sales(db_session, skip=0, limit=10)

        assert len(result) == 5
        for sale in result:
            assert sale.quantity > 0
            assert sale.total_amount > 0

    def test_get_sales_stats(self, db_session, multiple_sales):
        """Test getting sales statistics"""
        result = SalesService.get_sales_stats(db_session)

        assert result.total_sales == 5
        assert result.total_revenue > 0
        assert result.average_basket > 0

    def test_get_sales_by_region(self, db_session, multiple_sales):
        """Test getting sales by region"""
        result = SalesService.get_sales_by_region(db_session)

        assert len(result.regions) > 0
        for region in result.regions:
            assert region.region
            assert region.revenue > 0
            assert region.count > 0

    def test_get_top_products(self, db_session, multiple_sales):
        """Test getting top selling products"""
        result = SalesService.get_top_selling_products(db_session, limit=3)

        assert len(result.products) <= 3
        assert len(result.products) > 0

        # Check products are sorted by units sold
        for product in result.products:
            assert product.name
            assert product.units_sold > 0
