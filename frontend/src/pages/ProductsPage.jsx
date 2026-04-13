import { Tag } from "@carbon/react";
import { DataTableWrapper } from "../components/shared";
import { ErrorState, LoadingState, PageHeader } from "../components/ui";
import { useFetchData } from "../hooks";
import { apiClient } from "../services/api/";
import { formatCurrency } from "../utils/formatters";

function ProductsPage() {
  const {
    data: products,
    loading,
    error,
    refetch,
  } = useFetchData(() => apiClient.get("/products/"), []);

  const headers = [
    { key: "name", header: "Product Name", isSortable: true },
    { key: "category", header: "Category", isSortable: true },
    { key: "brand", header: "Brand", isSortable: true },
    { key: "price", header: "Price", isSortable: true },
    { key: "sku", header: "SKU", isSortable: true },
  ];

  const getCategoryColor = (category) => {
    const colors = {
      Skincare: "blue",
      Makeup: "magenta",
      Haircare: "teal",
      Fragrance: "purple",
      "Body Care": "cyan",
    };
    return colors[category] || "gray";
  };

  const rowMapper = (product) => ({
    id: product.id,
    name: product.name,
    category: (
      <Tag type={getCategoryColor(product.category)} size="sm">
        {product.category}
      </Tag>
    ),
    brand: product.brand,
    price: formatCurrency(product.price),
    sku: product.sku,
  });

  if (loading) return <LoadingState message="Loading products..." />;
  if (error) return <ErrorState message={error} onRetry={refetch} />;

  const productsData = Array.isArray(products) ? products : [];

  return (
    <div className="page-container">
      <PageHeader
        title="Products Catalog"
        subtitle="Browse and manage your cosmetics product inventory"
      />

      <DataTableWrapper
        data={productsData}
        headers={headers}
        rowMapper={rowMapper}
        searchPlaceholder="Search products..."
        initialSort={{ key: "name", direction: "ASC" }}
        pageSizes={[10, 20, 50, 100]}
        exportFilename="products"
        exportTitle="Products Catalog"
        tableId="products-table"
      />
    </div>
  );
}

export default ProductsPage;
