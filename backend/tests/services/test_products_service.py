"""
Tests for ProductsService
"""

from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.services.products_service import ProductsService


class TestProductsService:
    """Tests for ProductsService"""

    def test_get_all_products(self, db_session, multiple_products):
        """Test getting all products"""
        result = ProductsService.get_products(db_session, skip=0, limit=10)

        assert len(result) == 5
        for product in result:
            assert product.name
            assert product.category
            assert product.price > 0

    def test_get_all_products_with_pagination(self, db_session, multiple_products):
        """Test pagination"""
        result = ProductsService.get_products(db_session, skip=0, limit=2)
        assert len(result) == 2

        result = ProductsService.get_products(db_session, skip=2, limit=2)
        assert len(result) == 2

    def test_get_product_by_id(self, db_session, sample_product):
        """Test getting product by ID"""
        result = ProductsService.get_product_by_id(db_session, sample_product.id)

        assert result.name == sample_product.name
        assert result.category == sample_product.category
        assert result.price == float(sample_product.price)

    def test_get_product_by_id_not_found(self, db_session):
        """Test getting non-existent product"""
        with pytest.raises(HTTPException) as exc_info:
            ProductsService.get_product_by_id(db_session, uuid4())

        assert exc_info.value.status_code == 404

    def test_get_products_by_category(self, db_session, multiple_products):
        """Test getting products by category"""
        result = ProductsService.get_products_by_category(db_session, "Skincare")

        assert result.category == "Skincare"
        assert len(result.products) > 0
        assert result.count == len(result.products)
        for product in result.products:
            assert product.category == "Skincare"
