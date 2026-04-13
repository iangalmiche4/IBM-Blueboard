import { useState } from "react";
import { Column, Grid } from "@carbon/react";
import { DataTableWrapper, MetricCard } from "../components/shared";
import { ErrorState, LoadingState, PageHeader } from "../components/ui";
import { API_CONFIG } from "../config/api";
import { useFetchData } from "../hooks";
import { apiClient } from "../services/api/";
import { formatCurrency, formatDate } from "../utils/formatters";

function SalesPage() {
  const [channelData, setChannelData] = useState([]);
  const [regionData, setRegionData] = useState([]);

  const {
    data: sales,
    loading,
    error,
    refetch,
  } = useFetchData(
    () => apiClient.get(`/sales?limit=${API_CONFIG.DEFAULT_LIMIT}`),
    [],
    {
      onSuccess: (data) => {
        // Handle both old and new API formats
        let salesData;
        if (Array.isArray(data)) {
          salesData = data;
        } else if (data.sales) {
          salesData = data.sales;
        } else {
          salesData = [];
        }

        // Sort by date, most recent first
        if (salesData.length > 0) {
          salesData.sort(
            (a, b) => new Date(b.sale_date) - new Date(a.sale_date),
          );
        }

        // Aggregate by channel and region
        const channelAgg = {};
        const regionAgg = {};

        if (Array.isArray(salesData)) {
          salesData.forEach((sale) => {
            channelAgg[sale.channel] =
              (channelAgg[sale.channel] || 0) + parseFloat(sale.total_amount);
            regionAgg[sale.region] =
              (regionAgg[sale.region] || 0) + parseFloat(sale.total_amount);
          });
        }

        // Sort by alphabetical order
        setChannelData(
          Object.entries(channelAgg)
            .map(([channel, value]) => ({
              group: channel,
              value: value,
            }))
            .sort((a, b) => a.group.localeCompare(b.group)),
        );

        setRegionData(
          Object.entries(regionAgg)
            .map(([region, value]) => ({
              group: region,
              value: value,
            }))
            .sort((a, b) => a.group.localeCompare(b.group)),
        );
      },
    },
  );

  const headers = [
    { key: "sale_date", header: "Date", isSortable: true },
    { key: "product_name", header: "Product", isSortable: true },
    { key: "customer_name", header: "Customer", isSortable: true },
    { key: "quantity", header: "Quantity", isSortable: true },
    { key: "unit_price", header: "Unit Price", isSortable: true },
    { key: "total_amount", header: "Total", isSortable: true },
    { key: "channel", header: "Channel", isSortable: true },
    { key: "region", header: "Region", isSortable: true },
  ];

  const rowMapper = (sale) => {
    const productId = sale.product_id
      ? String(sale.product_id).substring(0, 8)
      : "N/A";
    const customerId = sale.customer_id
      ? String(sale.customer_id).substring(0, 8)
      : "N/A";

    return {
      id: sale.id,
      sale_date: formatDate(sale.sale_date),
      product_name: sale.product_name || `Product ${productId}`,
      customer_name: sale.customer_name || `Customer ${customerId}`,
      quantity: sale.quantity || 0,
      unit_price: formatCurrency(sale.unit_price || 0),
      total_amount: formatCurrency(sale.total_amount || 0),
      channel: sale.channel || "Unknown",
      region: sale.region || "Unknown",
    };
  };

  if (loading) return <LoadingState message="Loading sales data..." />;
  if (error) return <ErrorState message={error} onRetry={refetch} />;

  // Handle both old and new API formats for display
  let salesData;
  if (Array.isArray(sales)) {
    salesData = sales;
  } else if (sales?.sales) {
    salesData = sales.sales;
  } else {
    salesData = [];
  }

  return (
    <div className="page-container">
      <PageHeader
        title="Sales Analytics"
        subtitle="Detailed view of sales transactions and performance"
      />

      {/* Summary Cards */}
      <Grid narrow className="mb-2">
        <Column sm={4} md={8} lg={8} xlg={8} max={8}>
          <MetricCard
            title="Sales by Channel"
            data={channelData}
            emptyMessage="No channel data available"
          />
        </Column>
        <Column sm={4} md={8} lg={8} xlg={8} max={8}>
          <MetricCard
            title="Sales by Region"
            data={regionData}
            emptyMessage="No region data available"
          />
        </Column>
      </Grid>

      {/* Sales Table */}
      <DataTableWrapper
        data={salesData}
        headers={headers}
        rowMapper={rowMapper}
        searchPlaceholder="Search sales..."
        initialSort={{ key: "sale_date", direction: "DESC" }}
        exportFilename="sales"
        exportTitle="Sales Transactions"
        tableId="sales-table"
      />
    </div>
  );
}

export default SalesPage;
