"""
Tests for InventoryService
"""

from datetime import date
from uuid import uuid4

from app.models.inventory import Inventory
from app.services.inventory_service import InventoryService


class TestInventoryService:
    """Tests for InventoryService"""

    def test_get_all_inventory(self, db_session, sample_product):
        """Test getting all inventory items"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=100,
            reserved_quantity=10,
            warehouse_location="Warehouse A",
            last_restock_date=date.today(),
            reorder_level=20,
        )
        db_session.add(inventory)
        db_session.commit()

        result = InventoryService.get_all_inventory(db_session)
        assert len(result) == 1
        assert result[0].stock_quantity == 100

    def test_get_inventory_by_id(self, db_session, sample_product):
        """Test getting inventory by ID"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=50,
            warehouse_location="Warehouse B",
            reorder_level=10,
        )
        db_session.add(inventory)
        db_session.commit()

        result = InventoryService.get_inventory_by_id(db_session, inventory.id)
        assert result is not None
        assert result.stock_quantity == 50

    def test_get_inventory_by_product(self, db_session, sample_product):
        """Test getting inventory by product ID"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=75,
            warehouse_location="Warehouse C",
            reorder_level=15,
        )
        db_session.add(inventory)
        db_session.commit()

        result = InventoryService.get_inventory_by_product(
            db_session, sample_product.id
        )
        assert result is not None
        assert result.product_id == sample_product.id

    def test_get_inventory_with_products(self, db_session, sample_product):
        """Test getting inventory with product details"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=60,
            warehouse_location="Warehouse D",
            reorder_level=12,
        )
        db_session.add(inventory)
        db_session.commit()

        result = InventoryService.get_inventory_with_products(db_session)
        assert len(result) == 1
        assert result[0].product_name == sample_product.name

    def test_get_low_stock_alerts(self, db_session, sample_product):
        """Test getting low stock alerts"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=5,
            warehouse_location="Warehouse E",
            reorder_level=10,
        )
        db_session.add(inventory)
        db_session.commit()

        result = InventoryService.get_low_stock_alerts(db_session)
        assert len(result) == 1
        assert result[0].shortage == 5

    def test_get_inventory_stats(self, db_session, sample_product):
        """Test getting inventory statistics"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=100,
            reserved_quantity=20,
            warehouse_location="Warehouse F",
            reorder_level=15,
        )
        db_session.add(inventory)
        db_session.commit()

        result = InventoryService.get_inventory_stats(db_session)
        assert result.total_products == 1
        assert result.total_reserved == 20

    def test_get_inventory_by_warehouse(self, db_session, sample_product):
        """Test getting inventory by warehouse"""
        inventory = Inventory(
            id=uuid4(),
            product_id=sample_product.id,
            stock_quantity=80,
            warehouse_location="Warehouse G",
            reorder_level=10,
        )
        db_session.add(inventory)
        db_session.commit()

        result = InventoryService.get_inventory_by_warehouse(db_session, "Warehouse G")
        assert len(result) == 1
        assert result[0].warehouse_location == "Warehouse G"
