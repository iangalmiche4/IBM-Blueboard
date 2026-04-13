"""
Tests for customers endpoints
"""

from fastapi import status


class TestCustomersRouter:
    """Tests for customers endpoints"""

    def test_get_customers(self, client, sample_customer):
        """Test GET /api/v1/customers/"""
        response = client.get("/api/v1/customers/?limit=10&offset=0")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["email"] == sample_customer.email

    def test_get_customers_with_segment(self, client, sample_customer):
        """Test GET /api/v1/customers/ with segment filter"""
        response = client.get(f"/api/v1/customers/?segment={sample_customer.segment}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

    def test_get_customer_by_id(self, client, sample_customer, sample_sale):
        """Test GET /api/v1/customers/{id}"""
        response = client.get(f"/api/v1/customers/{sample_customer.id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert isinstance(data, dict)
        assert data["id"] == str(sample_customer.id)
        assert data["email"] == sample_customer.email
        assert "stats" in data
        assert data["stats"]["total_orders"] >= 1

    def test_get_segment_distribution(self, client, sample_customer):
        """Test GET /api/v1/customers/segments/distribution"""
        response = client.get("/api/v1/customers/segments/distribution")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "segments" in data
        assert len(data["segments"]) > 0
