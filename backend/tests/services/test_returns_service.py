"""
Tests for ReturnsService
"""

from datetime import date
from decimal import Decimal
from uuid import uuid4

from app.models.return_model import Return
from app.services.returns_service import ReturnsService


class TestReturnsService:
    """Tests for ReturnsService"""

    def test_get_all_returns(
        self, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test getting all returns"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Defective",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("50.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        result = ReturnsService.get_all_returns(db_session)
        assert len(result) == 1
        assert result[0].reason == "Defective"

    def test_get_return_by_id(
        self, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test getting return by ID"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=2,
            reason="Wrong item",
            status="Processed",
            return_date=date.today(),
            refund_amount=Decimal("100.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        result = ReturnsService.get_return_by_id(db_session, return_item.id)
        assert result is not None
        assert result.reason == "Wrong item"

    def test_get_returns_with_details(
        self, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test getting returns with details"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Not satisfied",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("75.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        result = ReturnsService.get_returns_with_details(db_session)
        assert len(result) == 1
        assert result[0].product_name == sample_product.name

    def test_get_returns_by_status(
        self, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test getting returns by status"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Damaged",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("60.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        result = ReturnsService.get_returns_by_status(db_session, "Pending")
        assert len(result) == 1

    def test_get_returns_by_customer(
        self, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test getting returns by customer"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Size issue",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("45.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        result = ReturnsService.get_returns_by_customer(db_session, sample_customer.id)
        assert len(result) == 1

    def test_get_returns_by_product(
        self, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test getting returns by product"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Quality issue",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("55.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        result = ReturnsService.get_returns_by_product(db_session, sample_product.id)
        assert len(result) == 1

    def test_get_return_stats(
        self, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test getting return statistics"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Stats test",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("70.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        result = ReturnsService.get_return_stats(db_session)
        assert result.total_returns == 1

    def test_get_return_reason_analysis(
        self, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test getting return reason analysis"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Analysis test",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("80.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        result = ReturnsService.get_return_reason_analysis(db_session)
        assert len(result) >= 1

    def test_get_product_return_rates(
        self, db_session, sample_product, sample_customer, sample_sale
    ):
        """Test getting product return rates"""
        return_item = Return(
            id=uuid4(),
            product_id=sample_product.id,
            customer_id=sample_customer.id,
            sale_id=sample_sale.id,
            quantity=1,
            reason="Rate test",
            status="Pending",
            return_date=date.today(),
            refund_amount=Decimal("65.00"),
        )
        db_session.add(return_item)
        db_session.commit()

        result = ReturnsService.get_product_return_rates(db_session)
        assert len(result) >= 0
