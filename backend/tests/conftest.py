"""
Pytest configuration and fixtures for backend tests

Uses a dedicated test PostgreSQL database with isolated credentials.
Test database and user are automatically created by init script 03-test-db.sql
"""

import os
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale
from app.models.satisfaction import Satisfaction

# Test database configuration - dedicated user and database for complete isolation
# Uses POSTGRES_TEST_* environment variables from .env
TEST_DB_USER = os.getenv("POSTGRES_TEST_USER", "blueboard_test")
TEST_DB_PASSWORD = os.getenv("POSTGRES_TEST_PASSWORD", "blueboard_password_test")
TEST_DB_HOST = os.getenv("POSTGRES_HOST", "database")
TEST_DB_PORT = os.getenv("POSTGRES_PORT", "5432")
TEST_DB_NAME = os.getenv("POSTGRES_TEST_DB", "blueboard_test")

SQLALCHEMY_DATABASE_URL = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create test database and tables, clean before tests"""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Clean all tables before running tests
    connection = engine.connect()
    transaction = connection.begin()

    try:
        # Delete all data from tables (in correct order to respect foreign keys)
        connection.execute(Satisfaction.__table__.delete())
        connection.execute(Sale.__table__.delete())
        connection.execute(Customer.__table__.delete())
        connection.execute(Product.__table__.delete())
        transaction.commit()
    except Exception:
        transaction.rollback()
        raise
    finally:
        connection.close()

    yield

    # Optionally drop all tables after tests (commented out to keep test data for inspection)
    # Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test

    Note: This uses the real PostgreSQL database.
    Data is rolled back after each test to keep tests isolated.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database session override"""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_product(db_session):
    """Create a sample product for testing"""
    product = Product(
        name="Test Product",
        category="Skincare",
        brand="Test Brand",
        price=29.99,
        sku="TEST-001",
        description="A test product",
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture
def sample_customer(db_session):
    """Create a sample customer for testing"""
    customer = Customer(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        birth_date=date(1990, 1, 1),
        gender="Male",
        segment="Premium",
        region="Île-de-France",
        registration_date=date.today() - timedelta(days=365),
        is_active=True,
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer


@pytest.fixture
def sample_sale(db_session, sample_product, sample_customer):
    """Create a sample sale for testing"""
    sale = Sale(
        product_id=sample_product.id,
        customer_id=sample_customer.id,
        quantity=2,
        unit_price=sample_product.price,
        total_amount=sample_product.price * 2,
        discount_amount=0,
        sale_date=date.today(),
        region=sample_customer.region,
        channel="Online",
        payment_method="Credit Card",
    )
    db_session.add(sale)
    db_session.commit()
    db_session.refresh(sale)
    return sale


@pytest.fixture
def sample_satisfaction(db_session, sample_product, sample_customer):
    """Create a sample satisfaction review for testing"""
    satisfaction = Satisfaction(
        product_id=sample_product.id,
        customer_id=sample_customer.id,
        overall_rating=5,
        quality_rating=5,
        price_rating=4,
        packaging_rating=4,
        delivery_rating=5,
        comment="Great product!",
        review_date=date.today(),
        verified_purchase=True,
        helpful_count=0,
    )
    db_session.add(satisfaction)
    db_session.commit()
    db_session.refresh(satisfaction)
    return satisfaction


@pytest.fixture
def multiple_products(db_session):
    """Create multiple products for testing"""
    products = [
        Product(
            name=f"Product {i}",
            category="Skincare" if i % 2 == 0 else "Makeup",
            brand=f"Brand {i}",
            price=10.0 + i * 5,
            sku=f"SKU-{i:03d}",
            description=f"Description for product {i}",
        )
        for i in range(1, 6)
    ]
    db_session.add_all(products)
    db_session.commit()
    for product in products:
        db_session.refresh(product)
    return products


@pytest.fixture
def multiple_sales(db_session, multiple_products, sample_customer):
    """Create multiple sales for testing"""
    sales = []
    for i, product in enumerate(multiple_products):
        sale = Sale(
            product_id=product.id,
            customer_id=sample_customer.id,
            quantity=i + 1,
            unit_price=product.price,
            total_amount=product.price * (i + 1),
            discount_amount=0,
            sale_date=date.today() - timedelta(days=i),
            region=sample_customer.region,
            channel="Online",
            payment_method="Credit Card",
        )
        sales.append(sale)

    db_session.add_all(sales)
    db_session.commit()
    for sale in sales:
        db_session.refresh(sale)
    return sales
