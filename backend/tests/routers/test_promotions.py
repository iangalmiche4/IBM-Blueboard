"""
Tests for promotions endpoints
"""

from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

from fastapi import status

from app.models.promotion import Promotion


class TestPromotionsRouter:
    """Tests for promotions endpoints"""

    def test_get_promotions(self, client, db_session, sample_sale):
        """Test GET /api/v1/promotions/"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="Test",
            discount_percentage=Decimal("15.00"),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )
        db_session.add(promotion)
        db_session.commit()

        response = client.get("/api/v1/promotions/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_promotions_with_sales(self, client, db_session, sample_sale):
        """Test GET /api/v1/promotions/with-sales"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="With Sales",
            discount_percentage=Decimal("20.00"),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=5),
        )
        db_session.add(promotion)
        db_session.commit()

        response = client.get("/api/v1/promotions/with-sales")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_active_promotions(self, client, db_session, sample_sale):
        """Test GET /api/v1/promotions/active"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="Active",
            discount_percentage=Decimal("25.00"),
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
        )
        db_session.add(promotion)
        db_session.commit()

        response = client.get("/api/v1/promotions/active")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_promotion_stats(self, client, db_session, sample_sale):
        """Test GET /api/v1/promotions/stats"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="Stats",
            discount_percentage=Decimal("10.00"),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
        )
        db_session.add(promotion)
        db_session.commit()

        response = client.get("/api/v1/promotions/stats")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_promotions" in data

    def test_get_promotion_roi(self, client, db_session, sample_sale):
        """Test GET /api/v1/promotions/roi"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="ROI",
            discount_percentage=Decimal("30.00"),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=4),
        )
        db_session.add(promotion)
        db_session.commit()

        response = client.get("/api/v1/promotions/roi")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_get_promotions_by_type(self, client, db_session, sample_sale):
        """Test GET /api/v1/promotions/type/{type}"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="Special",
            discount_percentage=Decimal("35.00"),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=6),
        )
        db_session.add(promotion)
        db_session.commit()

        response = client.get("/api/v1/promotions/type/Special")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_promotion_by_id(self, client, db_session, sample_sale):
        """Test GET /api/v1/promotions/{id}"""
        promotion = Promotion(
            id=uuid4(),
            sale_id=sample_sale.id,
            promo_type="By ID",
            discount_percentage=Decimal("18.00"),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=8),
        )
        db_session.add(promotion)
        db_session.commit()

        response = client.get(f"/api/v1/promotions/{promotion.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["promo_type"] == "By ID"

    def test_get_promotion_by_id_not_found(self, client):
        """Test GET /api/v1/promotions/{id} not found"""
        response = client.get(f"/api/v1/promotions/{uuid4()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
