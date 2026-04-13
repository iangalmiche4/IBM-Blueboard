import { Tag } from "@carbon/react";
import { DataTableWrapper } from "../components/shared";
import { ErrorState, LoadingState, PageHeader } from "../components/ui";
import { API_CONFIG } from "../config/api";
import { useFetchData } from "../hooks";
import { apiClient } from "../services/api/";
import { formatDate } from "../utils/formatters";

function CustomersPage() {
  const {
    data: customers,
    loading,
    error,
    refetch,
  } = useFetchData(
    () => apiClient.get(`/customers/?limit=${API_CONFIG.DEFAULT_LIMIT}`),
    [],
    {
      onSuccess: (data) => {
        // Ensure data is an array
        if (!Array.isArray(data)) {
          console.warn("Expected array but got:", typeof data);
        }
      },
    },
  );

  const headers = [
    { key: "customer_id", header: "Customer ID", isSortable: true },
    { key: "name", header: "Customer Name", isSortable: true },
    { key: "email", header: "Email", isSortable: true },
    { key: "segment", header: "Segment", isSortable: true },
    { key: "region", header: "Region", isSortable: true },
    { key: "registration_date", header: "Registration Date", isSortable: true },
    { key: "is_active", header: "Status", isSortable: true },
  ];

  const getSegmentColor = (segment) => {
    const colors = {
      VIP: "purple",
      Premium: "blue",
      Regular: "green",
      Occasional: "cyan",
      New: "gray",
    };
    return colors[segment] || "gray";
  };

  const rowMapper = (customer) => ({
    id: customer.id,
    customer_id: customer.id.substring(0, 8) + "...",
    name: `${customer.first_name} ${customer.last_name}`,
    email: customer.email,
    segment: (
      <Tag type={getSegmentColor(customer.segment)} size="sm">
        {customer.segment}
      </Tag>
    ),
    region: customer.region,
    registration_date: formatDate(customer.registration_date),
    is_active: (
      <Tag type={customer.is_active ? "green" : "red"} size="sm">
        {customer.is_active ? "Active" : "Inactive"}
      </Tag>
    ),
  });

  if (loading) return <LoadingState message="Loading customers..." />;
  if (error) return <ErrorState message={error} onRetry={refetch} />;

  const customersData = Array.isArray(customers) ? customers : [];

  return (
    <div className="page-container">
      <PageHeader
        title="Customers"
        subtitle="Manage your customer base and segments"
      />

      <DataTableWrapper
        data={customersData}
        headers={headers}
        rowMapper={rowMapper}
        searchPlaceholder="Search customers..."
        initialSort={{ key: "name", direction: "ASC" }}
        pageSizes={[10, 20, 50, 100]}
        exportFilename="customers"
        exportTitle="Customers List"
        tableId="customers-table"
      />
    </div>
  );
}

export default CustomersPage;
