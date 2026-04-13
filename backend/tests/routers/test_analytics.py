"""
Tests for analytics endpoints
"""

from fastapi import status


class TestAnalyticsRouter:
    """Tests for analytics endpoints"""

    def test_get_dashboard(self, client, sample_sale, sample_satisfaction):
        """Test GET /api/v1/analytics/dashboard"""
        response = client.get("/api/v1/analytics/dashboard")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "kpis" in data
        assert "timestamp" in data
        assert data["kpis"]["total_revenue"] > 0
        assert data["kpis"]["total_sales"] == 1
        assert data["kpis"]["avg_satisfaction"] > 0

    def test_get_sales_trends(self, client, multiple_sales):
        """Test GET /api/v1/analytics/sales-trends"""
        response = client.get("/api/v1/analytics/sales-trends")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "trends" in data
        assert len(data["trends"]) > 0

    def test_get_top_products(self, client, multiple_sales):
        """Test GET /api/v1/analytics/top-products"""
        response = client.get("/api/v1/analytics/top-products?limit=3")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "products" in data
        assert len(data["products"]) <= 3

    def test_get_top_products_invalid_limit(self, client):
        """Test top products with invalid limit"""
        response = client.get("/api/v1/analytics/top-products?limit=0")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_category_distribution(self, client, multiple_sales):
        """Test GET /api/v1/analytics/category-distribution"""
        response = client.get("/api/v1/analytics/category-distribution")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "distribution" in data
        assert len(data["distribution"]) > 0

    def test_get_satisfaction_stats(self, client, sample_satisfaction):
        """Test GET /api/v1/analytics/satisfaction-stats"""
        response = client.get("/api/v1/analytics/satisfaction-stats")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "average_ratings" in data
        assert data["average_ratings"]["overall"] > 0

    def test_get_regional_performance(self, client, multiple_sales):
        """Test GET /api/v1/analytics/regional-performance"""
        response = client.get("/api/v1/analytics/regional-performance")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "regions" in data
        assert len(data["regions"]) > 0

    def test_get_kpi_trends(self, client, multiple_sales, sample_satisfaction):
        """Test GET /api/v1/analytics/kpi-trends"""
        response = client.get("/api/v1/analytics/kpi-trends")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "total_revenue" in data
        assert "total_sales" in data
        assert "avg_satisfaction" in data
        assert "avg_basket" in data
        assert "period_days" in data

        # Check structure of each KPI trend
        for kpi in ["total_revenue", "total_sales", "avg_satisfaction", "avg_basket"]:
            assert "current" in data[kpi]
            assert "previous" in data[kpi]
            assert "change_percentage" in data[kpi]
            assert isinstance(data[kpi]["current"], (int, float))
            assert isinstance(data[kpi]["previous"], (int, float))
            assert isinstance(data[kpi]["change_percentage"], (int, float))

    def test_get_kpi_trends_custom_period(self, client, multiple_sales):
        """Test KPI trends with custom period"""
        response = client.get("/api/v1/analytics/kpi-trends?period_days=7")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["period_days"] == 7

    def test_get_kpi_trends_invalid_period(self, client):
        """Test KPI trends with invalid period"""
        response = client.get("/api/v1/analytics/kpi-trends?period_days=0")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_quick_stats(
        self, client, sample_product, sample_customer, multiple_sales
    ):
        """Test GET /api/v1/analytics/quick-stats"""
        response = client.get("/api/v1/analytics/quick-stats")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "active_products" in data
        assert "active_customers" in data
        assert "avg_order_value" in data
        assert "return_rate" in data

        assert isinstance(data["active_products"], int)
        assert isinstance(data["active_customers"], int)
        assert isinstance(data["avg_order_value"], (int, float))
        assert isinstance(data["return_rate"], (int, float))

        # Return rate should be between 0 and 1
        assert 0 <= data["return_rate"] <= 1

        # Should have at least one active product and customer
        assert data["active_products"] >= 1
        assert data["active_customers"] >= 1
