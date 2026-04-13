"""
Analytics schemas - Pydantic models for API responses
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class KPIData(BaseModel):
    """Dashboard KPI metrics"""

    total_revenue: float = Field(..., description="Total revenue in currency")
    total_sales: int = Field(..., description="Total number of sales")
    avg_satisfaction: float = Field(
        ..., ge=0, le=5, description="Average satisfaction rating"
    )
    total_customers: int = Field(..., description="Total number of customers")
    avg_basket: float = Field(..., description="Average basket value")


class DashboardResponse(BaseModel):
    """Complete dashboard data response"""

    kpis: KPIData
    timestamp: datetime


class SalesTrendItem(BaseModel):
    """Sales trend data point"""

    month: str = Field(..., description="Month in YYYY-MM format")
    revenue: float = Field(..., description="Total revenue for the month")
    count: int = Field(..., description="Number of sales")


class SalesTrendsResponse(BaseModel):
    """Sales trends over time"""

    trends: List[SalesTrendItem]


class TopProductItem(BaseModel):
    """Top product data"""

    name: str
    category: str
    brand: str
    revenue: float
    units_sold: int


class TopProductsResponse(BaseModel):
    """Top selling products"""

    products: List[TopProductItem]


class CategoryDistributionItem(BaseModel):
    """Category distribution data"""

    category: str
    revenue: float
    count: int


class CategoryDistributionResponse(BaseModel):
    """Sales distribution by category"""

    distribution: List[CategoryDistributionItem]


class AverageRatings(BaseModel):
    """Average satisfaction ratings by criteria"""

    overall: float = Field(..., ge=0, le=5)
    quality: float = Field(..., ge=0, le=5)
    price: float = Field(..., ge=0, le=5)
    packaging: float = Field(..., ge=0, le=5)
    delivery: float = Field(..., ge=0, le=5)


class SatisfactionStatsResponse(BaseModel):
    """Satisfaction statistics"""

    average_ratings: AverageRatings


class RegionalPerformanceItem(BaseModel):
    """Regional performance data"""

    region: str
    revenue: float
    count: int


class RegionalPerformanceResponse(BaseModel):
    """Sales performance by region"""

    regions: List[RegionalPerformanceItem]


class KPITrendItem(BaseModel):
    """KPI trend data with current and previous values"""

    current: float = Field(..., description="Current period value")
    previous: float = Field(..., description="Previous period value")
    change_percentage: float = Field(..., description="Percentage change")


class KPITrendsResponse(BaseModel):
    """KPI trends with historical comparison"""

    total_revenue: KPITrendItem
    total_sales: KPITrendItem
    avg_satisfaction: KPITrendItem
    avg_basket: KPITrendItem
    period_days: int = Field(
        default=30, description="Number of days in comparison period"
    )


class QuickStatsResponse(BaseModel):
    """Quick statistics for dashboard"""

    active_products: int = Field(..., description="Number of active products")
    active_customers: int = Field(..., description="Number of active customers")
    avg_order_value: float = Field(..., description="Average order value")
    return_rate: float = Field(
        ..., ge=0, le=1, description="Return rate as decimal (0-1)"
    )
