"""
Tests for inventory endpoints
"""

from uuid import uuid4

from fastapi import status

from app.models.inventory import Inventory


class TestInventoryRouter:
    """Tests for inventory endpoints"""

    def test_get_inventory(self, client, db_session, sample_product):
        """Test GET /api/v1/inventory/"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=100,
            warehouse_location="Warehouse A",
            reorder_level=20,
        )
        db_session.add(inventory)
        db_session.commit()

        response = client.get("/api/v1/inventory/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_inventory_with_products(self, client, db_session, sample_product):
        """Test GET /api/v1/inventory/with-products"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=50,
            warehouse_location="Warehouse B",
            reorder_level=10,
        )
        db_session.add(inventory)
        db_session.commit()

        response = client.get("/api/v1/inventory/with-products")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert "product_name" in data[0]

    def test_get_low_stock_alerts(self, client, db_session, sample_product):
        """Test GET /api/v1/inventory/low-stock"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=5,
            warehouse_location="Warehouse C",
            reorder_level=10,
        )
        db_session.add(inventory)
        db_session.commit()

        response = client.get("/api/v1/inventory/low-stock")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_inventory_stats(self, client, db_session, sample_product):
        """Test GET /api/v1/inventory/stats"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=100,
            warehouse_location="Warehouse D",
            reorder_level=15,
        )
        db_session.add(inventory)
        db_session.commit()

        response = client.get("/api/v1/inventory/stats")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_products" in data

    def test_get_inventory_by_warehouse(self, client, db_session, sample_product):
        """Test GET /api/v1/inventory/warehouse/{warehouse}"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=75,
            warehouse_location="Warehouse E",
            reorder_level=12,
        )
        db_session.add(inventory)
        db_session.commit()

        response = client.get("/api/v1/inventory/warehouse/Warehouse E")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_inventory_by_id(self, client, db_session, sample_product):
        """Test GET /api/v1/inventory/{id}"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=60,
            warehouse_location="Warehouse F",
            reorder_level=10,
        )
        db_session.add(inventory)
        db_session.commit()

        response = client.get(f"/api/v1/inventory/{inventory.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["stock_quantity"] == 60

    def test_get_inventory_by_id_not_found(self, client):
        """Test GET /api/v1/inventory/{id} not found"""
        response = client.get(f"/api/v1/inventory/{uuid4()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_inventory_by_product(self, client, db_session, sample_product):
        """Test GET /api/v1/inventory/product/{product_id}"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=80,
            warehouse_location="Warehouse G",
            reorder_level=15,
        )
        db_session.add(inventory)
        db_session.commit()

        response = client.get(f"/api/v1/inventory/product/{sample_product.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["product_id"] == str(sample_product.id)

    def test_get_inventory_by_product_not_found(self, client):
        """Test GET /api/v1/inventory/product/{product_id} not found"""
        response = client.get(f"/api/v1/inventory/product/{uuid4()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
