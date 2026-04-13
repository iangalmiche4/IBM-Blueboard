"""
Tests for SatisfactionService
"""

from uuid import uuid4

from app.models.product import Product
from app.services.satisfaction_service import SatisfactionService


class TestSatisfactionService:
    """Tests for SatisfactionService"""

    def test_get_all_reviews(self, db_session, sample_satisfaction):
        """Test getting all reviews"""
        result = SatisfactionService.get_reviews(db_session, skip=0, limit=10)

        assert len(result) == 1
        assert result[0].overall_rating == sample_satisfaction.overall_rating
        assert result[0].comment == sample_satisfaction.comment

    def test_get_satisfaction_stats(self, db_session, sample_satisfaction):
        """Test getting satisfaction statistics"""

    def test_get_product_reviews_empty(self, db_session):
        """Test getting reviews for product with no reviews"""
        new_product = Product(
            id=uuid4(),
            name="New Product",
            category="Test",
            price=100.0,
            sku="TEST001",
            brand="TestBrand",
            description="Test product",
        )
        db_session.add(new_product)
        db_session.commit()

        result = SatisfactionService.get_product_reviews(db_session, new_product.id)

        assert result.product_id == str(new_product.id)
        assert result.average_rating == 0.0
        assert result.count == 0
        assert len(result.reviews) == 0

    def test_get_product_reviews(self, db_session, sample_satisfaction, sample_product):
        """Test getting reviews for a specific product"""
        result = SatisfactionService.get_product_reviews(db_session, sample_product.id)

        assert len(result.reviews) == 1
        assert result.reviews[0].overall_rating == sample_satisfaction.overall_rating

    def test_get_average_satisfaction(self, db_session, sample_satisfaction):
        """Test getting average satisfaction"""
        result = SatisfactionService.get_average_satisfaction(db_session)

        assert result.average_rating > 0
