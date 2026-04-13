"""
Inventory service - Business logic for inventory management
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.product import Product
from app.schemas.inventory import InventoryStats, InventoryWithProduct, LowStockAlert


class InventoryService:
    """Service for inventory operations"""

    @staticmethod
    def get_all_inventory(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[Inventory]:
        """Get all inventory items"""
        return db.query(Inventory).offset(skip).limit(limit).all()

    @staticmethod
    def get_inventory_by_id(db: Session, inventory_id: UUID) -> Optional[Inventory]:
        """Get inventory by ID"""
        return db.query(Inventory).filter(Inventory.id == inventory_id).first()

    @staticmethod
    def get_inventory_by_product(db: Session, product_id: UUID) -> Optional[Inventory]:
        """Get inventory by product ID"""
        return db.query(Inventory).filter(Inventory.product_id == product_id).first()

    @staticmethod
    def get_inventory_with_products(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[InventoryWithProduct]:
        """Get inventory with product details"""
        results = (
            db.query(
                Inventory,
                Product.name.label("product_name"),
                Product.category.label("product_category"),
                Product.sku.label("product_sku"),
            )
            .join(Product, Inventory.product_id == Product.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [
            InventoryWithProduct(
                id=inv.id,
                product_id=inv.product_id,
                stock_quantity=inv.stock_quantity,
                reserved_quantity=inv.reserved_quantity,
                warehouse_location=inv.warehouse_location,
                last_restock_date=inv.last_restock_date,
                reorder_level=inv.reorder_level,
                updated_at=inv.updated_at,
                product_name=product_name,
                product_category=product_category,
                product_sku=product_sku,
            )
            for inv, product_name, product_category, product_sku in results
        ]

    @staticmethod
    def get_low_stock_alerts(db: Session) -> List[LowStockAlert]:
        """Get products with stock below reorder level"""
        results = (
            db.query(
                Inventory,
                Product.name.label("product_name"),
                Product.sku.label("product_sku"),
            )
            .join(Product, Inventory.product_id == Product.id)
            .filter(Inventory.stock_quantity <= Inventory.reorder_level)
            .all()
        )

        return [
            LowStockAlert(
                product_id=inv.product_id,
                product_name=product_name,
                product_sku=product_sku,
                stock_quantity=inv.stock_quantity,
                reorder_level=inv.reorder_level,
                warehouse_location=inv.warehouse_location,
                shortage=inv.reorder_level - inv.stock_quantity,
            )
            for inv, product_name, product_sku in results
        ]

    @staticmethod
    def get_inventory_stats(db: Session) -> InventoryStats:
        """Get inventory statistics"""
        # Total products in inventory
        total_products = db.query(func.count(Inventory.id)).scalar() or 0

        # Total stock value (stock_quantity * product price)
        total_stock_value = (
            db.query(func.sum(Inventory.stock_quantity * Product.price))
            .join(Product, Inventory.product_id == Product.id)
            .scalar()
            or 0.0
        )

        # Low stock items (stock <= reorder level)
        low_stock_items = (
            db.query(func.count(Inventory.id))
            .filter(Inventory.stock_quantity <= Inventory.reorder_level)
            .scalar()
            or 0
        )

        # Out of stock items
        out_of_stock_items = (
            db.query(func.count(Inventory.id))
            .filter(Inventory.stock_quantity == 0)
            .scalar()
            or 0
        )

        # Total reserved quantity
        total_reserved = db.query(func.sum(Inventory.reserved_quantity)).scalar() or 0

        # Number of warehouses
        warehouses_count = (
            db.query(func.count(func.distinct(Inventory.warehouse_location))).scalar()
            or 0
        )

        return InventoryStats(
            total_products=total_products,
            total_stock_value=float(total_stock_value),
            low_stock_items=low_stock_items,
            out_of_stock_items=out_of_stock_items,
            total_reserved=total_reserved,
            warehouses_count=warehouses_count,
        )

    @staticmethod
    def get_inventory_by_warehouse(db: Session, warehouse: str) -> List[Inventory]:
        """Get inventory by warehouse location"""
        return (
            db.query(Inventory).filter(Inventory.warehouse_location == warehouse).all()
        )
