"""
Analytics service - Business logic for analytics operations
"""

from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Customer, Product, Return, Sale, Satisfaction
from app.schemas.analytics import (
    AverageRatings,
    CategoryDistributionItem,
    CategoryDistributionResponse,
    DashboardResponse,
    KPIData,
    KPITrendItem,
    KPITrendsResponse,
    QuickStatsResponse,
    RegionalPerformanceItem,
    RegionalPerformanceResponse,
    SalesTrendItem,
    SalesTrendsResponse,
    SatisfactionStatsResponse,
    TopProductItem,
    TopProductsResponse,
)


class AnalyticsService:
    """Service for analytics operations"""

    @staticmethod
    def get_dashboard_data(db: Session) -> DashboardResponse:
        """
        Calculate and return complete dashboard KPIs

        Args:
            db: Database session

        Returns:
            DashboardResponse with all KPIs
        """
        # Calculate KPIs
        total_revenue = db.query(func.sum(Sale.total_amount)).scalar() or 0
        total_sales = db.query(func.count(Sale.id)).scalar() or 0
        avg_satisfaction = db.query(func.avg(Satisfaction.overall_rating)).scalar() or 0
        total_customers = db.query(func.count(Customer.id)).scalar() or 0

        # Calculate average basket
        avg_basket = total_revenue / total_sales if total_sales > 0 else 0

        kpis = KPIData(
            total_revenue=float(total_revenue),
            total_sales=total_sales,
            avg_satisfaction=round(float(avg_satisfaction), 2),
            total_customers=total_customers,
            avg_basket=round(float(avg_basket), 2),
        )

        return DashboardResponse(kpis=kpis, timestamp=datetime.utcnow())

    @staticmethod
    def get_sales_trends(db: Session) -> SalesTrendsResponse:
        """
        Get sales trends aggregated by month

        Args:
            db: Database session

        Returns:
            SalesTrendsResponse with monthly trends
        """
        results = (
            db.query(
                func.date_trunc("month", Sale.sale_date).label("month"),
                func.sum(Sale.total_amount).label("revenue"),
                func.count(Sale.id).label("count"),
            )
            .group_by("month")
            .order_by("month")
            .all()
        )

        trends = [
            SalesTrendItem(
                month=r.month.strftime("%Y-%m"), revenue=float(r.revenue), count=r.count
            )
            for r in results
        ]

        return SalesTrendsResponse(trends=trends)

    @staticmethod
    def get_top_products(db: Session, limit: int = 10) -> TopProductsResponse:
        """
        Get top selling products by revenue

        Args:
            db: Database session
            limit: Maximum number of products to return

        Returns:
            TopProductsResponse with top products
        """
        results = (
            db.query(
                Product.name,
                Product.category,
                Product.brand,
                func.sum(Sale.total_amount).label("revenue"),
                func.sum(Sale.quantity).label("units_sold"),
            )
            .join(Sale)
            .group_by(Product.id, Product.name, Product.category, Product.brand)
            .order_by(func.sum(Sale.total_amount).desc())
            .limit(limit)
            .all()
        )

        products = [
            TopProductItem(
                name=r.name,
                category=r.category,
                brand=r.brand,
                revenue=float(r.revenue),
                units_sold=r.units_sold,
            )
            for r in results
        ]

        return TopProductsResponse(products=products)

    @staticmethod
    def get_category_distribution(db: Session) -> CategoryDistributionResponse:
        """
        Get sales distribution by product category

        Args:
            db: Database session

        Returns:
            CategoryDistributionResponse with distribution data
        """
        results = (
            db.query(
                Product.category,
                func.sum(Sale.total_amount).label("revenue"),
                func.count(Sale.id).label("count"),
            )
            .join(Sale)
            .group_by(Product.category)
            .all()
        )

        distribution = [
            CategoryDistributionItem(
                category=r.category, revenue=float(r.revenue), count=r.count
            )
            for r in results
        ]

        return CategoryDistributionResponse(distribution=distribution)

    @staticmethod
    def get_satisfaction_stats(db: Session) -> SatisfactionStatsResponse:
        """
        Get satisfaction statistics by criteria

        Args:
            db: Database session

        Returns:
            SatisfactionStatsResponse with average ratings
        """
        avg_ratings = db.query(
            func.avg(Satisfaction.overall_rating).label("overall"),
            func.avg(Satisfaction.quality_rating).label("quality"),
            func.avg(Satisfaction.price_rating).label("price"),
            func.avg(Satisfaction.packaging_rating).label("packaging"),
            func.avg(Satisfaction.delivery_rating).label("delivery"),
        ).first()

        ratings = AverageRatings(
            overall=round(float(avg_ratings.overall or 0), 2),
            quality=round(float(avg_ratings.quality or 0), 2),
            price=round(float(avg_ratings.price or 0), 2),
            packaging=round(float(avg_ratings.packaging or 0), 2),
            delivery=round(float(avg_ratings.delivery or 0), 2),
        )

        return SatisfactionStatsResponse(average_ratings=ratings)

    @staticmethod
    def get_regional_performance(db: Session) -> RegionalPerformanceResponse:
        """
        Get sales performance by region

        Args:
            db: Database session

        Returns:
            RegionalPerformanceResponse with regional data
        """
        results = (
            db.query(
                Sale.region,
                func.sum(Sale.total_amount).label("revenue"),
                func.count(Sale.id).label("count"),
            )
            .group_by(Sale.region)
            .order_by(func.sum(Sale.total_amount).desc())
            .all()
        )

        regions = [
            RegionalPerformanceItem(
                region=r.region, revenue=float(r.revenue), count=r.count
            )
            for r in results
        ]

        return RegionalPerformanceResponse(regions=regions)

    @staticmethod
    def get_kpi_trends(db: Session, period_days: int = 30) -> KPITrendsResponse:
        """
        Get KPI trends with historical comparison

        Args:
            db: Database session
            period_days: Number of days for comparison period (default: 30)

        Returns:
            KPITrendsResponse with current vs previous period comparison
        """
        now = datetime.utcnow()
        current_start = now - timedelta(days=period_days)
        previous_start = current_start - timedelta(days=period_days)

        # Current period KPIs
        current_revenue = (
            db.query(func.sum(Sale.total_amount))
            .filter(Sale.sale_date >= current_start)
            .scalar()
            or 0
        )

        current_sales = (
            db.query(func.count(Sale.id))
            .filter(Sale.sale_date >= current_start)
            .scalar()
            or 0
        )

        current_satisfaction = (
            db.query(func.avg(Satisfaction.overall_rating))
            .filter(Satisfaction.review_date >= current_start)
            .scalar()
            or 0
        )

        current_basket = current_revenue / current_sales if current_sales > 0 else 0

        # Previous period KPIs
        previous_revenue = (
            db.query(func.sum(Sale.total_amount))
            .filter(Sale.sale_date >= previous_start, Sale.sale_date < current_start)
            .scalar()
            or 0
        )

        previous_sales = (
            db.query(func.count(Sale.id))
            .filter(Sale.sale_date >= previous_start, Sale.sale_date < current_start)
            .scalar()
            or 0
        )

        previous_satisfaction = (
            db.query(func.avg(Satisfaction.overall_rating))
            .filter(
                Satisfaction.review_date >= previous_start,
                Satisfaction.review_date < current_start,
            )
            .scalar()
            or 0
        )

        previous_basket = previous_revenue / previous_sales if previous_sales > 0 else 0

        # Calculate percentage changes
        def calc_change(current: float, previous: float) -> float:
            if previous == 0:
                return 0.0
            return ((current - previous) / previous) * 100

        return KPITrendsResponse(
            total_revenue=KPITrendItem(
                current=float(current_revenue),
                previous=float(previous_revenue),
                change_percentage=round(
                    calc_change(current_revenue, previous_revenue), 2
                ),
            ),
            total_sales=KPITrendItem(
                current=float(current_sales),
                previous=float(previous_sales),
                change_percentage=round(calc_change(current_sales, previous_sales), 2),
            ),
            avg_satisfaction=KPITrendItem(
                current=round(float(current_satisfaction), 2),
                previous=round(float(previous_satisfaction), 2),
                change_percentage=round(
                    calc_change(current_satisfaction, previous_satisfaction), 2
                ),
            ),
            avg_basket=KPITrendItem(
                current=round(float(current_basket), 2),
                previous=round(float(previous_basket), 2),
                change_percentage=round(
                    calc_change(current_basket, previous_basket), 2
                ),
            ),
            period_days=period_days,
        )

    @staticmethod
    def get_quick_stats(db: Session) -> QuickStatsResponse:
        """
        Get quick statistics for dashboard

        Args:
            db: Database session

        Returns:
            QuickStatsResponse with quick stats
        """
        # Total products count (Product model doesn't have is_active field)
        active_products = db.query(func.count(Product.id)).scalar() or 0

        # Active customers count
        active_customers = (
            db.query(func.count(Customer.id))
            .filter(Customer.is_active == True)
            .scalar()
            or 0
        )

        # Average order value (same as avg_basket)
        total_revenue = db.query(func.sum(Sale.total_amount)).scalar() or 0
        total_sales = db.query(func.count(Sale.id)).scalar() or 0
        avg_order_value = total_revenue / total_sales if total_sales > 0 else 0

        # Return rate (returns / sales)
        total_returns = db.query(func.count(Return.id)).scalar() or 0
        return_rate = total_returns / total_sales if total_sales > 0 else 0

        return QuickStatsResponse(
            active_products=active_products,
            active_customers=active_customers,
            avg_order_value=round(float(avg_order_value), 2),
            return_rate=round(float(return_rate), 4),
        )
