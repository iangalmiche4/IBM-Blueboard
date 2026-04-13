"""
Tests for returns endpoints
"""

from datetime import date
from decimal import Decimal
from uuid import uuid4

from fastapi import status

from app.models.return_model import Return


class TestReturnsRouter:
    """Tests for returns endpoints"""

    def test_get_returns(
        self, client, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test GET /api/v1/returns/"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Test",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("50.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        response = client.get("/api/v1/returns/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_returns_with_details(
        self, client, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test GET /api/v1/returns/with-details"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Details test",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("60.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        response = client.get("/api/v1/returns/with-details")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_return_stats(
        self, client, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test GET /api/v1/returns/stats"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Stats",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("70.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        response = client.get("/api/v1/returns/stats")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_returns" in data

    def test_get_return_reason_analysis(
        self, client, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test GET /api/v1/returns/reason-analysis"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Analysis",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("80.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        response = client.get("/api/v1/returns/reason-analysis")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_get_product_return_rates(
        self, client, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test GET /api/v1/returns/product-rates"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Rates",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("90.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        response = client.get("/api/v1/returns/product-rates")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_get_returns_by_status(
        self, client, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test GET /api/v1/returns/status/{status}"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Status test",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("55.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        response = client.get("/api/v1/returns/status/Pending")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_returns_by_customer(
        self, client, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test GET /api/v1/returns/customer/{customer_id}"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Customer test",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("65.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        response = client.get(f"/api/v1/returns/customer/{sample_customer.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_returns_by_product(
        self, client, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test GET /api/v1/returns/product/{product_id}"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Product test",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("75.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        response = client.get(f"/api/v1/returns/product/{sample_product.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_return_by_id(
        self, client, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test GET /api/v1/returns/{id}"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="By ID",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("85.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        response = client.get(f"/api/v1/returns/{return_item.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["reason"] == "By ID"

    def test_get_return_by_id_not_found(self, client):
        """Test GET /api/v1/returns/{id} not found"""
        response = client.get(f"/api/v1/returns/{uuid4()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
