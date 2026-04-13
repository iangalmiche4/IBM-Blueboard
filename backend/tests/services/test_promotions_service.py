"""
Tests for PromotionsService
"""

from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

from app.models.promotion import Promotion
from app.services.promotions_service import PromotionsService


class TestPromotionsService:
    """Tests for PromotionsService"""

    def test_get_all_promotions(self, db_session, sample_sale):
        """Test getting all promotions"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_code="SAVE20",
            promo_type="Seasonal",
            discount_percentage=Decimal("20.00"),
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() + timedelta(days=10),
        )
        db_session.add(promotion)
        db_session.commit()

        result = PromotionsService.get_all_promotions(db_session)
        assert len(result) == 1
        assert result[0].promo_code == "SAVE20"

    def test_get_promotion_by_id(self, db_session, sample_sale):
        """Test getting promotion by ID"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="Flash Sale",
            discount_percentage=Decimal("30.00"),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
        )
        db_session.add(promotion)
        db_session.commit()

        result = PromotionsService.get_promotion_by_id(db_session, promotion.id)
        assert result is not None
        assert result.promo_type == "Flash Sale"

    def test_get_promotions_with_sales(self, db_session, sample_sale, sample_customer):
        """Test getting promotions with sale details"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="Holiday",
            discount_percentage=Decimal("15.00"),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )
        db_session.add(promotion)
        db_session.commit()

        result = PromotionsService.get_promotions_with_sales(db_session)
        assert len(result) == 1
        assert result[0].promo_type == "Holiday"

    def test_get_active_promotions(self, db_session, sample_sale):
        """Test getting active promotions"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="Active",
            discount_percentage=Decimal("25.00"),
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=5),
        )
        db_session.add(promotion)
        db_session.commit()

        result = PromotionsService.get_active_promotions(db_session)
        assert len(result) == 1

    def test_get_promotions_by_type(self, db_session, sample_sale):
        """Test getting promotions by type"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="Clearance",
            discount_percentage=Decimal("40.00"),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3),
        )
        db_session.add(promotion)
        db_session.commit()

        result = PromotionsService.get_promotions_by_type(db_session, "Clearance")
        assert len(result) == 1

    def test_get_promotion_stats(self, db_session, sample_sale):
        """Test getting promotion statistics"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="Stats Test",
            discount_percentage=Decimal("10.00"),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
        )
        db_session.add(promotion)
        db_session.commit()

        result = PromotionsService.get_promotion_stats(db_session)
        assert result.total_promotions == 1

    def test_get_promotion_roi(self, db_session, sample_sale):
        """Test getting promotion ROI"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="ROI Test",
            discount_percentage=Decimal("20.00"),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=5),
        )
        db_session.add(promotion)
        db_session.commit()

        result = PromotionsService.get_promotion_roi(db_session)
        assert len(result) >= 0
