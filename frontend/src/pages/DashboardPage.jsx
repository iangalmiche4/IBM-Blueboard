import { Reset } from "@carbon/icons-react";
import { Button } from "@carbon/react";
import {
  DraggableDashboardGrid,
  InfoTile,
  KPITile,
  MuiBarChart,
  MuiPieChart,
  WidgetContainer,
} from "../components/dashboard";
import RechartsWidget from "../components/dashboard/RechartsWidget";
import { ErrorState, LoadingState, PageHeader } from "../components/ui";
import { dashboardConfig } from "../config/dashboardConfig";
import { useDashboardData } from "../hooks";
import { formatCurrency, formatNumber } from "../utils/formatters";

function DashboardPage() {
  const {
    loading,
    error,
    kpis,
    salesTrends,
    kpiTrends,
    quickStats,
    channelPerformance,
    regionDistribution,
    promotionRoi,
  } = useDashboardData();

  if (loading) return <LoadingState message="Loading dashboard..." />;
  if (error) return <ErrorState message={error} />;

  // Helper function to format values based on formatter type
  const formatValue = (value, formatter) => {
    if (!value && value !== 0) return "-";
    if (typeof formatter === "function") return formatter(value);
    if (formatter === "currency") return formatCurrency(value);
    if (formatter === "number") return formatNumber(value);
    return value;
  };

  // Render individual KPI tile with dynamic trends
  const renderKPITile = (kpiId) => {
    const config = dashboardConfig.kpis.find((k) => k.id === kpiId);
    if (!config || !kpis || !kpiTrends) return null;

    const value = kpis[config.dataKey];
    const formattedValue = formatValue(value, config.formatter);

    // Use real trend data from backend
    const trendData = kpiTrends[config.dataKey];
    const change = trendData ? trendData.change_percentage : 0;

    return (
      <KPITile
        title={config.title}
        subtitle={config.subtitle}
        value={formattedValue}
        icon={config.icon}
        change={change}
      />
    );
  };

  // Render Quick Stats with dynamic data
  const renderQuickStats = () => {
    const config = dashboardConfig.quickStats;
    if (!quickStats) return null;

    return (
      <InfoTile title={config.title} icon={config.icon} className="full-height">
        <p>
          <strong>Active Products:</strong>{" "}
          {formatNumber(quickStats.active_products)}
        </p>
        <p>
          <strong>Active Customers:</strong>{" "}
          {formatNumber(quickStats.active_customers)}
        </p>
        <p>
          <strong>Avg Order Value:</strong>{" "}
          {formatCurrency(quickStats.avg_order_value)}
        </p>
        <p>
          <strong>Return Rate:</strong>{" "}
          {(quickStats.return_rate * 100).toFixed(2)}%
        </p>
      </InfoTile>
    );
  };

  // Reset dashboard layout
  const handleResetLayout = () => {
    if (window.resetDashboardLayout) {
      window.resetDashboardLayout();
      window.location.reload();
    }
  };

  return (
    <div className="page-container">
      <PageHeader
        title="Dashboard"
        subtitle="Overview of your cosmetics business performance - Drag widgets to customize layout"
        actions={
          <Button
            kind="ghost"
            size="sm"
            renderIcon={Reset}
            iconDescription="Reset layout"
            hasIconOnly
            onClick={handleResetLayout}
            tooltipPosition="left"
          />
        }
      />

      <DraggableDashboardGrid>
        <div key="kpi-revenue">
          <WidgetContainer id="kpi-revenue">
            {renderKPITile("total_revenue")}
          </WidgetContainer>
        </div>

        <div key="kpi-sales">
          <WidgetContainer id="kpi-sales">
            {renderKPITile("total_sales")}
          </WidgetContainer>
        </div>

        <div key="kpi-satisfaction">
          <WidgetContainer id="kpi-satisfaction">
            {renderKPITile("avg_satisfaction")}
          </WidgetContainer>
        </div>

        <div key="kpi-basket">
          <WidgetContainer id="kpi-basket">
            {renderKPITile("avg_basket")}
          </WidgetContainer>
        </div>

        <div key="chart-sales-trends">
          <WidgetContainer id="chart-sales-trends">
            <RechartsWidget
              title={dashboardConfig.charts.salesTrends.title}
              data={salesTrends}
              emptyMessage="No data available"
            />
          </WidgetContainer>
        </div>

        <div key="chart-channels">
          <WidgetContainer id="chart-channels">
            <MuiBarChart
              title="Channel Performance"
              data={channelPerformance}
              height={280}
              xAxisKey="label"
              yAxisKey="value"
            />
          </WidgetContainer>
        </div>

        <div key="chart-regions">
          <WidgetContainer id="chart-regions">
            <MuiPieChart
              title="Sales by Region"
              data={regionDistribution}
              height={280}
              outerRadius={90}
            />
          </WidgetContainer>
        </div>

        <div key="kpi-stats">
          <WidgetContainer id="kpi-stats">{renderQuickStats()}</WidgetContainer>
        </div>


        {/* Analyse du ROI des Promotions */}
        <div key="promotion_roi">
          <WidgetContainer id="promotion_roi">
            <MuiBarChart
              title="Promotion ROI Analysis"
              data={promotionRoi}
              height={280}
              xAxisKey="label"
              yAxisKey="value"
              yAxisFormatter={(value) => `${value}%`}
              valueFormatter={(value) => `${value}%`}
            />
          </WidgetContainer>
        </div>

      </DraggableDashboardGrid>
    </div>
  );
}

export default DashboardPage;
