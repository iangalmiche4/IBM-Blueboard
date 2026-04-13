"""
Tests for satisfaction endpoints
"""

from fastapi import status


class TestSatisfactionRouter:
    """Tests for satisfaction endpoints"""

    def test_get_reviews(self, client, sample_satisfaction):
        """Test GET /api/v1/satisfaction/"""
        response = client.get("/api/v1/satisfaction/?limit=10&offset=0")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["overall_rating"] == sample_satisfaction.overall_rating

    def test_get_satisfaction_stats(self, client, sample_satisfaction):
        """Test GET /api/v1/satisfaction/stats"""
        response = client.get("/api/v1/satisfaction/stats")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "total_reviews" in data
        assert data["total_reviews"] == 1

    def test_get_product_reviews(self, client, sample_satisfaction, sample_product):
        """Test GET /api/v1/satisfaction/by-product/{id}"""
        response = client.get(f"/api/v1/satisfaction/by-product/{sample_product.id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "reviews" in data
        assert len(data["reviews"]) == 1

    def test_get_average_satisfaction(self, client, sample_satisfaction):
        """Test GET /api/v1/satisfaction/average"""
        response = client.get("/api/v1/satisfaction/average")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "average_rating" in data
        assert data["average_rating"] > 0
        assert "total_reviews" in data
        assert data["total_reviews"] == 1
