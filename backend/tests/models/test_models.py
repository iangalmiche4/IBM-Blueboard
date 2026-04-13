"""
Tests for database models __repr__ methods
"""

from datetime import date
from decimal import Decimal

from app.models.customer import Customer
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.promotion import Promotion
from app.models.return_model import Return
from app.models.sale import Sale
from app.models.satisfaction import Satisfaction


class TestModelRepresentations:
    """Test __repr__ methods of all models"""

    def test_customer_repr(self, db_session):
        """Test Customer __repr__"""
        customer = Customer(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            segment="Premium",
            region="Île-de-France",
            registration_date=date(2024, 1, 15),
            is_active=True,
        )
        db_session.add(customer)
        db_session.commit()

        repr_str = repr(customer)
        assert "Customer" in repr_str
        assert customer.email in repr_str

    def test_product_repr(self, db_session):
        """Test Product __repr__"""
        product = Product(
            name="Test Product",
            category="Skincare",
            brand="Test Brand",
            price=Decimal("29.99"),
            sku="TEST-001",
            description="A test product",
        )
        db_session.add(product)
        db_session.commit()

        repr_str = repr(product)
        assert "Product" in repr_str
        assert product.name in repr_str

    def test_sale_repr(self, db_session):
        """Test Sale __repr__"""
        # Create dependencies first
        customer = Customer(
            email="sale@example.com",
            first_name="Jane",
            last_name="Smith",
            segment="Standard",
            region="Provence-Alpes-Côte d'Azur",
            registration_date=date(2024, 1, 1),
            is_active=True,
        )
        product = Product(
            name="Sale Product",
            category="Makeup",
            brand="Sale Brand",
            price=Decimal("49.99"),
            sku="SALE-001",
            description="Product for sale",
        )
        db_session.add(customer)
        db_session.add(product)
        db_session.commit()

        sale = Sale(
            customer_id=customer.id,
            product_id=product.id,
            quantity=2,
            unit_price=Decimal("49.99"),
            total_amount=Decimal("99.98"),
            discount_amount=Decimal("0.00"),
            sale_date=date.today(),
            region="Île-de-France",
            payment_method="Credit Card",
            channel="Online",
        )
        db_session.add(sale)
        db_session.commit()

        repr_str = repr(sale)
        assert "Sale" in repr_str
        assert str(sale.total_amount) in repr_str

    def test_satisfaction_repr(self, db_session):
        """Test Satisfaction __repr__"""
        # Create dependencies
        customer = Customer(
            email="satisfaction@example.com",
            first_name="Robert",
            last_name="Johnson",
            segment="Premium",
            region="Nouvelle-Aquitaine",
            registration_date=date(2024, 1, 1),
            is_active=True,
        )
        product = Product(
            name="Satisfaction Product",
            category="Fragrance",
            brand="Satisfaction Brand",
            price=Decimal("79.99"),
            sku="SAT-001",
            description="Product for satisfaction",
        )
        db_session.add(customer)
        db_session.add(product)
        db_session.commit()

        satisfaction = Satisfaction(
            customer_id=customer.id,
            product_id=product.id,
            overall_rating=5,
            quality_rating=5,
            price_rating=4,
            packaging_rating=5,
            delivery_rating=4,
            comment="Great product!",
            review_date=date.today(),
            verified_purchase=True,
        )
        db_session.add(satisfaction)
        db_session.commit()

        repr_str = repr(satisfaction)
        assert "Satisfaction" in repr_str
        assert str(satisfaction.overall_rating) in repr_str

    def test_inventory_repr(self, db_session, sample_product):
        """Test Inventory __repr__"""
        inventory = Inventory(
            product_id=sample_product.id,
            stock_quantity=100,
            reserved_quantity=10,
            warehouse_location="A1",
            reorder_level=20,
        )
        db_session.add(inventory)
        db_session.commit()

        repr_str = repr(inventory)
        assert "Inventory" in repr_str
        assert "100" in repr_str

    def test_promotion_repr(self, db_session, sample_sale):
        """Test Promotion __repr__"""
        promotion = Promotion(
            sale_id=sample_sale.id,
            promo_code="SUMMER2024",
            promo_type="Seasonal",
            discount_percentage=Decimal("15.00"),
            start_date=date(2024, 6, 1),
            end_date=date(2024, 8, 31),
        )
        db_session.add(promotion)
        db_session.commit()

        repr_str = repr(promotion)
        assert "Promotion" in repr_str
        assert "Seasonal" in repr_str
        assert "15" in repr_str

    def test_return_repr(
        self, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test Return __repr__"""
        return_obj = Return(
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Defective",
            status="Approved",
            return_date=date.today(),
            refund_amount=Decimal("50.00"),
        )
        db_session.add(return_obj)
        db_session.commit()

        repr_str = repr(return_obj)
        assert "Return" in repr_str
        assert "Approved" in repr_str
