import {
  Analytics,
  Currency,
  FaceAdd,
  Receipt,
  ShoppingCart,
} from "@carbon/icons-react";

// Configuration for dashboard widgets
export const dashboardConfig = {
  kpis: [
    {
      id: "total_revenue",
      title: "Total Revenue",
      subtitle: "Last 30 days",
      icon: Currency,
      dataKey: "total_revenue",
      formatter: "currency",
    },
    {
      id: "total_sales",
      title: "Total Sales",
      subtitle: "Number of transactions",
      icon: ShoppingCart,
      dataKey: "total_sales",
      formatter: "number",
    },
    {
      id: "avg_satisfaction",
      title: "Avg Satisfaction",
      subtitle: "Customer rating",
      icon: FaceAdd,
      dataKey: "avg_satisfaction",
      formatter: (value) => `${value.toFixed(1)}/5`,
    },
    {
      id: "avg_basket",
      title: "Avg Basket",
      subtitle: "Per transaction",
      icon: Receipt,
      dataKey: "avg_basket",
      formatter: "currency",
    },
  ],
  charts: {
    salesTrends: {
      id: "sales_trends",
      title: "Sales Trends",
      type: "line",
      options: {
        axes: {
          bottom: {
            title: "Month",
            mapsTo: "date",
            scaleType: "time",
          },
          left: {
            title: "Revenue (€)",
            mapsTo: "value",
            scaleType: "linear",
          },
        },
        curve: "curveMonotoneX",
        height: "100%",
        theme: "white",
        color: {
          scale: {
            Revenue: "#0f62fe",
          },
        },
        legend: {
          enabled: false,
        },
      },
    },
  },
  quickStats: {
    id: "quick_stats",
    title: "Quick Stats",
    icon: Analytics,
    // All data now comes from API - no hardcoded values
  },
};

// Grid layout configuration
export const gridLayout = {
  zones: [
    {
      id: "top-left",
      widgets: ["total_revenue", "total_sales"],
    },
    {
      id: "top-right",
      widgets: ["avg_satisfaction", "avg_basket"],
    },
    {
      id: "middle-full",
      widgets: ["promotion_roi"],
    },
    {
      id: "bottom-left",
      widgets: ["sales_trends"],
    },
    {
      id: "bottom-right",
      widgets: ["quick_stats"],
    },
  ],
};
