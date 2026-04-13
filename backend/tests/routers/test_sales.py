"""
Tests for sales endpoints
"""

from fastapi import status


class TestSalesRouter:
    """Tests for sales endpoints"""

    def test_get_sales(self, client, multiple_sales):
        """Test GET /api/v1/sales/"""
        response = client.get("/api/v1/sales/?limit=10&offset=0")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 5

    def test_get_sales_stats(self, client, multiple_sales):
        """Test GET /api/v1/sales/stats"""
        response = client.get("/api/v1/sales/stats")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "total_sales" in data
        assert "total_revenue" in data
        assert data["total_sales"] == 5

    def test_get_sales_by_region(self, client, multiple_sales):
        """Test GET /api/v1/sales/by-region"""
        response = client.get("/api/v1/sales/by-region")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "regions" in data
        assert len(data["regions"]) > 0

    def test_get_top_products(self, client, multiple_sales):
        """Test GET /api/v1/sales/top-products"""
        response = client.get("/api/v1/sales/top-products?limit=3")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "products" in data
        assert len(data["products"]) <= 3
