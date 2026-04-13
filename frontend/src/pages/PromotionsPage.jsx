import {
  ChartAverage,
  CheckmarkFilled,
  Currency,
  Point,
  Purchase,
} from "@carbon/icons-react";
import { Column, Grid, Tag } from "@carbon/react";
import { KPITile } from "../components/dashboard";
import { TopPromotionsROI } from "../components/promotions";
import { DataTableWrapper } from "../components/shared";
import { ErrorState, LoadingState, PageHeader } from "../components/ui";
import { useFetchData } from "../hooks";
import { promotionsAPI } from "../services/api/";
import {
  formatCurrency,
  formatDate,
  formatPercentage,
} from "../utils/formatters";

function PromotionsPage() {
  const {
    data: promotions,
    loading: promotionsLoading,
    error: promotionsError,
    refetch: refetchPromotions,
  } = useFetchData(() => promotionsAPI.getWithSales(), []);

  const {
    data: stats,
    loading: statsLoading,
    error: statsError,
  } = useFetchData(() => promotionsAPI.getStats(), []);

  const {
    data: roi,
    loading: roiLoading,
    error: roiError,
  } = useFetchData(() => promotionsAPI.getROI(), []);

  const headers = [
    { key: "promo_code", header: "Promo Code", isSortable: true },
    { key: "promo_type", header: "Type", isSortable: true },
    { key: "discount_percentage", header: "Discount", isSortable: true },
    { key: "start_date", header: "Start Date", isSortable: true },
    { key: "end_date", header: "End Date", isSortable: true },
    { key: "usage_count", header: "Usage", isSortable: true },
    { key: "total_revenue", header: "Revenue", isSortable: true },
    { key: "status", header: "Status", isSortable: true },
  ];

  const loading = promotionsLoading || statsLoading || roiLoading;
  const error = promotionsError || statsError || roiError;

  const getPromotionStatus = (promo) => {
    const now = new Date();
    const start = new Date(promo.start_date);
    const end = new Date(promo.end_date);

    if (now < start) return { label: "Scheduled", type: "blue" };
    if (now > end) return { label: "Expired", type: "gray" };
    return { label: "Active", type: "green" };
  };

  const getTypeColor = (type) => {
    const colors = {
      Percentage: "purple",
      "Fixed Amount": "cyan",
      BOGO: "magenta",
      "Free Shipping": "teal",
    };
    return colors[type] || "gray";
  };

  const rowMapper = (promo) => {
    const status = getPromotionStatus(promo);
    const totalRevenue =
      promo.sales?.reduce(
        (sum, sale) => sum + parseFloat(sale.total_amount || 0),
        0,
      ) || 0;

    return {
      id: promo.id,
      promo_code: promo.promo_code,
      promo_type: (
        <Tag type={getTypeColor(promo.promo_type)} size="sm">
          {promo.promo_type}
        </Tag>
      ),
      discount_percentage: formatPercentage(promo.discount_percentage / 100),
      start_date: formatDate(promo.start_date),
      end_date: formatDate(promo.end_date),
      usage_count: promo.sales?.length || 0,
      total_revenue: formatCurrency(totalRevenue),
      status: (
        <Tag type={status.type} size="sm">
          {status.label}
        </Tag>
      ),
    };
  };

  if (loading) return <LoadingState message="Loading promotions data..." />;
  if (error) return <ErrorState message={error} onRetry={refetchPromotions} />;

  // Add calculated status to promotions data for sorting
  const promotionsData = Array.isArray(promotions)
    ? promotions.map((promo) => ({
        ...promo,
        status: getPromotionStatus(promo).label,
      }))
    : [];
  const roiData = Array.isArray(roi) ? roi : [];

  return (
    <div className="page-container">
      <PageHeader
        title="Promotions Dashboard"
        subtitle="Track promotional campaigns, discount codes, and marketing ROI"
      />

      {stats && (
        <Grid className="metrics-grid">
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Total Promotions"
              subtitle="All campaigns"
              value={stats.total_promotions}
              icon={Purchase}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Active Promotions"
              subtitle="Currently running"
              value={stats.active_promotions}
              icon={CheckmarkFilled}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Avg Discount"
              subtitle="Across all promotions"
              value={formatPercentage(stats.average_discount / 100)}
              icon={ChartAverage}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Total Usage"
              subtitle="Times promotions used"
              value={stats.total_usage}
              icon={Point}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Total Revenue"
              subtitle="From promotional sales"
              value={formatCurrency(stats.total_revenue)}
              icon={Currency}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Avg Revenue/Promo"
              subtitle="Per campaign"
              value={formatCurrency(stats.average_revenue_per_promotion)}
              icon={ChartAverage}
            />
          </Column>
        </Grid>
      )}

      <TopPromotionsROI promotions={roiData} maxItems={3} />

      <DataTableWrapper
        data={promotionsData}
        headers={headers}
        rowMapper={rowMapper}
        searchPlaceholder="Search promotions..."
        initialSort={{ key: "start_date", direction: "DESC" }}
        pageSizes={[10, 20, 50, 100]}
        exportFilename="promotions"
        exportTitle="Promotions Report"
        tableId="promotions-table"
      />
    </div>
  );
}

export default PromotionsPage;
