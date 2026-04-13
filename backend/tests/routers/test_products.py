"""
Tests for products endpoints
"""

from uuid import uuid4

from fastapi import status


class TestProductsRouter:
    """Tests for products endpoints"""

    def test_get_products(self, client, multiple_products):
        """Test GET /api/v1/products/"""
        response = client.get("/api/v1/products/?limit=10&offset=0")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 5
        assert "name" in data[0]
        assert "category" in data[0]

    def test_get_products_pagination(self, client, multiple_products):
        """Test products pagination"""
        response = client.get("/api/v1/products/?limit=2&offset=0")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

    def test_get_product_by_id(self, client, sample_product):
        """Test GET /api/v1/products/{id}"""
        response = client.get(f"/api/v1/products/{sample_product.id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["name"] == sample_product.name
        assert data["category"] == sample_product.category
        assert data["price"] == float(sample_product.price)

    def test_get_product_by_id_not_found(self, client):
        """Test getting non-existent product"""
        fake_id = str(uuid4())

        response = client.get(f"/api/v1/products/{fake_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_products_by_category(self, client, multiple_products):
        """Test GET /api/v1/products/category/{category}"""
        response = client.get("/api/v1/products/category/Skincare")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "category" in data
        assert data["category"] == "Skincare"
        assert "products" in data
        assert len(data["products"]) > 0
