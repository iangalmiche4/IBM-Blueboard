import {
  Cube,
  Currency,
  InventoryManagement,
  ShoppingCartArrowDown,
  ShoppingCartError,
  ShoppingCartMinus,
} from "@carbon/icons-react";
import { Column, Grid, Tag } from "@carbon/react";
import { KPITile } from "../components/dashboard";
import { AlertCard, DataTableWrapper } from "../components/shared";
import {
  AlertSection,
  ErrorState,
  LoadingState,
  PageHeader,
} from "../components/ui";
import { useFetchData } from "../hooks";
import { inventoryAPI } from "../services/api/";
import { formatCurrency, formatDate, formatNumber } from "../utils/formatters";

function InventoryPage() {
  const {
    data: inventory,
    loading: inventoryLoading,
    error: inventoryError,
    refetch: refetchInventory,
  } = useFetchData(() => inventoryAPI.getWithProducts(), []);

  const {
    data: stats,
    loading: statsLoading,
    error: statsError,
  } = useFetchData(() => inventoryAPI.getStats(), []);

  const {
    data: lowStockAlerts,
    loading: alertsLoading,
    error: alertsError,
  } = useFetchData(() => inventoryAPI.getLowStockAlerts(10), []);

  const headers = [
    { key: "product_name", header: "Product", isSortable: true },
    { key: "warehouse_location", header: "Warehouse", isSortable: true },
    { key: "stock_quantity", header: "Stock", isSortable: true },
    { key: "reserved_quantity", header: "Reserved", isSortable: true },
    { key: "available_quantity", header: "Available", isSortable: true },
    { key: "reorder_level", header: "Reorder Level", isSortable: true },
    { key: "last_restock_date", header: "Last Restock", isSortable: true },
    { key: "status", header: "Status", isSortable: true },
  ];

  const loading = inventoryLoading || statsLoading || alertsLoading;
  const error = inventoryError || statsError || alertsError;

  const getStockStatus = (item) => {
    const available = item.stock_quantity - item.reserved_quantity;
    if (available <= 0) return { label: "Out of Stock", type: "red" };
    if (available <= item.reorder_level)
      return { label: "Low Stock", type: "red" };
    return { label: "In Stock", type: "green" };
  };

  const rowMapper = (item) => {
    const status = getStockStatus(item);
    const available = item.stock_quantity - item.reserved_quantity;

    return {
      id: item.id,
      product_name: item.product_id,
      warehouse_location: item.warehouse_location,
      stock_quantity: formatNumber(item.stock_quantity),
      reserved_quantity: formatNumber(item.reserved_quantity),
      available_quantity: (
        <span className={available <= item.reorder_level ? "font-bold" : ""}>
          {formatNumber(available)}
        </span>
      ),
      reorder_level: formatNumber(item.reorder_level),
      last_restock_date: formatDate(item.last_restock_date),
      status: (
        <Tag type={status.type} size="sm">
          {status.label}
        </Tag>
      ),
    };
  };

  if (loading) return <LoadingState message="Loading inventory data..." />;
  if (error) return <ErrorState message={error} onRetry={refetchInventory} />;

  // Add calculated status to inventory data for sorting
  const inventoryData = Array.isArray(inventory)
    ? inventory.map((item) => ({
        ...item,
        status: getStockStatus(item).label,
      }))
    : [];
  const alertsData = Array.isArray(lowStockAlerts) ? lowStockAlerts : [];

  return (
    <div className="page-container">
      <PageHeader
        title="Inventory Management"
        subtitle="Monitor stock levels, warehouse locations, and reorder alerts"
      />

      {stats && (
        <Grid className="metrics-grid">
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Total Products"
              subtitle="Unique products in inventory"
              value={formatNumber(stats.total_products || 0)}
              icon={Cube}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Stock Value"
              subtitle="Total inventory value"
              value={formatCurrency(stats.total_stock_value || 0)}
              icon={Currency}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Warehouses"
              subtitle="Storage locations"
              value={formatNumber(stats.warehouses_count || 0)}
              icon={InventoryManagement}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Reserved Stock"
              subtitle="Units pending orders"
              value={formatNumber(stats.total_reserved || 0)}
              icon={ShoppingCartArrowDown}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Low Stock Items"
              subtitle="Below reorder level"
              value={formatNumber(stats.low_stock_items || 0)}
              icon={ShoppingCartMinus}
            />
          </Column>
          <Column sm={4} md={4} lg={4}>
            <KPITile
              title="Out of Stock"
              subtitle="Items unavailable"
              value={formatNumber(stats.out_of_stock_items || 0)}
              icon={ShoppingCartError}
            />
          </Column>
        </Grid>
      )}

      <AlertSection
        title={`Low Stock Alerts (${alertsData.length})`}
        description="The following items are at or below their reorder level and need restocking:"
        items={alertsData}
        renderItem={(item) => (
          <AlertCard
            key={item.product_id}
            title={item.product_name}
            fields={[
              { label: "Location", value: item.warehouse_location },
              { label: "Stock", value: `${item.stock_quantity} units` },
              { label: "Reorder Level", value: item.reorder_level },
              { label: "Shortage", value: item.shortage },
            ]}
          />
        )}
      />

      <DataTableWrapper
        data={inventoryData}
        headers={headers}
        rowMapper={rowMapper}
        searchPlaceholder="Search inventory..."
        initialSort={{ key: "product_name", direction: "ASC" }}
        pageSizes={[10, 20, 50, 100]}
        exportFilename="inventory"
        exportTitle="Inventory Report"
        tableId="inventory-table"
      />
    </div>
  );
}

export default InventoryPage;
