"""
Analytics router - Main dashboard data endpoints
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.analytics import (
    CategoryDistributionResponse,
    DashboardResponse,
    KPITrendsResponse,
    QuickStatsResponse,
    RegionalPerformanceResponse,
    SalesTrendsResponse,
    SatisfactionStatsResponse,
    TopProductsResponse,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard_data(db: Session = Depends(get_db)):
    """
    Get complete dashboard data including KPIs and chart data
    """
    return AnalyticsService.get_dashboard_data(db)


@router.get("/sales-trends", response_model=SalesTrendsResponse)
async def get_sales_trends(db: Session = Depends(get_db)):
    """
    Get sales trends over time (monthly aggregation)
    """
    return AnalyticsService.get_sales_trends(db)


@router.get("/top-products", response_model=TopProductsResponse)
async def get_top_products(
    limit: int = Query(
        10000, ge=1, le=10000, description="Number of products to return"
    ),
    db: Session = Depends(get_db),
):
    """
    Get top selling products by revenue
    """
    return AnalyticsService.get_top_products(db, limit)


@router.get("/category-distribution", response_model=CategoryDistributionResponse)
async def get_category_distribution(db: Session = Depends(get_db)):
    """
    Get sales distribution by product category
    """
    return AnalyticsService.get_category_distribution(db)


@router.get("/satisfaction-stats", response_model=SatisfactionStatsResponse)
async def get_satisfaction_stats(db: Session = Depends(get_db)):
    """
    Get satisfaction statistics by criteria
    """
    return AnalyticsService.get_satisfaction_stats(db)


@router.get("/regional-performance", response_model=RegionalPerformanceResponse)
async def get_regional_performance(db: Session = Depends(get_db)):
    """
    Get sales performance by region
    """
    return AnalyticsService.get_regional_performance(db)


@router.get("/kpi-trends", response_model=KPITrendsResponse)
async def get_kpi_trends(
    period_days: int = Query(
        30, ge=1, le=365, description="Number of days for comparison period"
    ),
    db: Session = Depends(get_db),
):
    """
    Get KPI trends with historical comparison

    Returns current vs previous period comparison for all main KPIs:
    - Total Revenue
    - Total Sales
    - Average Satisfaction
    - Average Basket
    """
    return AnalyticsService.get_kpi_trends(db, period_days)


@router.get("/quick-stats", response_model=QuickStatsResponse)
async def get_quick_stats(db: Session = Depends(get_db)):
    """
    Get quick statistics for dashboard

    Returns:
    - Active products count
    - Active customers count
    - Average order value
    - Return rate
    """
    return AnalyticsService.get_quick_stats(db)
