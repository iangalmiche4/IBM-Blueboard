import {
  ChartAverage,
  ChartLine,
  CheckmarkFilled,
  Currency,
  Renew,
  ShoppingCartArrowUp,
} from "@carbon/icons-react";
import { Column, Grid, Tag } from "@carbon/react";
import { KPITile } from "../components/dashboard";
import { TopReturnReasons } from "../components/returns";
import { AlertCard, DataTableWrapper } from "../components/shared";
import {
  AlertSection,
  ErrorState,
  LoadingState,
  PageHeader,
} from "../components/ui";
import { useFetchData } from "../hooks";
import { returnsAPI } from "../services/api/";
import {
  formatCurrency,
  formatDate,
  formatPercentage,
} from "../utils/formatters";

function ReturnsPage() {
  const {
    data: returns,
    loading: returnsLoading,
    error: returnsError,
    refetch: refetchReturns,
  } = useFetchData(() => returnsAPI.getWithDetails(), []);

  const {
    data: stats,
    loading: statsLoading,
    error: statsError,
  } = useFetchData(() => returnsAPI.getStats(), []);

  const {
    data: reasonAnalysis,
    loading: reasonsLoading,
    error: reasonsError,
  } = useFetchData(() => returnsAPI.getReasonAnalysis(), []);

  const {
    data: productReturnRates,
    loading: ratesLoading,
    error: ratesError,
  } = useFetchData(() => returnsAPI.getProductReturnRates(), []);

  const headers = [
    { key: "customer_name", header: "Customer", isSortable: true },
    { key: "product_name", header: "Product", isSortable: true },
    { key: "quantity", header: "Quantity", isSortable: true },
    { key: "reason", header: "Reason", isSortable: true },
    { key: "return_date", header: "Return Date", isSortable: true },
    { key: "refund_amount", header: "Refund", isSortable: true },
    { key: "status", header: "Status", isSortable: true },
  ];

  const loading =
    returnsLoading || statsLoading || reasonsLoading || ratesLoading;
  const error = returnsError || statsError || reasonsError || ratesError;

  const getStatusColor = (status) => {
    const colors = {
      Pending: "blue",
      Approved: "green",
      Rejected: "red",
      Refunded: "purple",
      Processing: "cyan",
    };
    return colors[status] || "gray";
  };

  const getReasonColor = (reason) => {
    const colors = {
      Defective: "red",
      "Wrong Item": "magenta",
      "Not as Described": "warm-gray",
      "Changed Mind": "blue",
      "Better Price Elsewhere": "cyan",
      "Quality Issues": "red",
      "Damaged in Transit": "red",
    };
    return colors[reason] || "gray";
  };

  const rowMapper = (returnItem) => ({
    id: returnItem.id,
    customer_name: returnItem.customer_name || "Unknown Customer",
    product_name: returnItem.product_name || "Unknown Product",
    quantity: returnItem.quantity,
    reason: (
      <Tag type={getReasonColor(returnItem.reason)} size="sm">
        {returnItem.reason}
      </Tag>
    ),
    return_date: formatDate(returnItem.return_date),
    refund_amount: formatCurrency(returnItem.refund_amount),
    status: (
      <Tag type={getStatusColor(returnItem.status)} size="sm">
        {returnItem.status}
      </Tag>
    ),
  });

  if (loading) return <LoadingState message="Loading returns data..." />;
  if (error) return <ErrorState message={error} onRetry={refetchReturns} />;

  const returnsData = Array.isArray(returns) ? returns : [];
  const reasonsData = Array.isArray(reasonAnalysis) ? reasonAnalysis : [];
  const ratesData = Array.isArray(productReturnRates) ? productReturnRates : [];

  return (
    <div className="page-container">
      <PageHeader
        title="Returns Analytics"
        subtitle="Monitor product returns, analyze reasons, and track refund impact"
      />

      {stats && (
        <Grid className="metrics-grid">
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Total Returns"
              subtitle="All time"
              value={stats.total_returns}
              icon={ShoppingCartArrowUp}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Return Rate"
              subtitle="Of total sales"
              value={formatPercentage(stats.return_rate)}
              icon={ChartLine}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Pending Returns"
              subtitle="Awaiting processing"
              value={stats.pending_returns}
              icon={Renew}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Approved Returns"
              subtitle="Ready for refund"
              value={stats.approved_returns}
              icon={CheckmarkFilled}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Total Refunded"
              subtitle="Financial impact"
              value={formatCurrency(stats.total_refund_amount)}
              icon={Currency}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Avg Refund"
              subtitle="Per return"
              value={formatCurrency(stats.average_refund_amount)}
              icon={ChartAverage}
            />
          </Column>
        </Grid>
      )}

      {reasonsData.length > 0 && (
        <TopReturnReasons
          reasons={reasonsData}
          getReasonColor={getReasonColor}
          maxItems={5}
        />
      )}

      <AlertSection
        title="Products with High Return Rates"
        description="These products have return rates above 15% and may need quality review:"
        items={ratesData.filter((p) => p.return_rate > 0.15).slice(0, 3)}
        renderMode="grid"
        renderItem={(product) => (
          <AlertCard
            key={product.product_id}
            title={product.product_name}
            fields={[
              {
                label: "Return Rate",
                value: formatPercentage(product.return_rate),
              },
              {
                label: "Returns",
                value: `${product.total_returned} / ${product.total_sold} sales`,
              },
              {
                label: "Refunded",
                value: formatCurrency(product.total_refund),
              },
            ]}
          />
        )}
      />

      <DataTableWrapper
        data={returnsData}
        headers={headers}
        rowMapper={rowMapper}
        searchPlaceholder="Search returns..."
        initialSort={{ key: "return_date", direction: "DESC" }}
        pageSizes={[10, 20, 50, 100]}
        exportFilename="returns"
        exportTitle="Returns Report"
        tableId="returns-table"
      />
    </div>
  );
}

export default ReturnsPage;
