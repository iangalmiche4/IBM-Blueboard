import { useEffect, useState } from "react";
import { API_CONFIG } from "../config/api";
import { apiClient } from "../services/api/";

function useAdvancedAnalyticsData() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    avgPrice: 0,
    avgRating: 0,
    totalRevenue: 0,
    activeCustomers: 0,
  });
  const [topProducts, setTopProducts] = useState([]);
  const [segmentData, setSegmentData] = useState([]);
  const [channelData, setChannelData] = useState([]);

  const fetchAdvancedAnalytics = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all data in parallel
      const [productsRes, salesRes, satisfactionRes, customersRes] =
        await Promise.all([
          apiClient.get(`/products?limit=${API_CONFIG.DEFAULT_LIMIT}`),
          apiClient.get(`/sales?limit=${API_CONFIG.DEFAULT_LIMIT}`),
          apiClient.get(`/satisfaction/?limit=${API_CONFIG.DEFAULT_LIMIT}`),
          apiClient.get(`/customers?limit=${API_CONFIG.DEFAULT_LIMIT}`),
        ]);

      const products = Array.isArray(productsRes.data) ? productsRes.data : [];
      const sales = Array.isArray(salesRes.data) ? salesRes.data : [];
      const reviews = Array.isArray(satisfactionRes.data)
        ? satisfactionRes.data
        : [];
      const customers = Array.isArray(customersRes.data)
        ? customersRes.data
        : [];

      // Calculate stats with safety checks
      const avgPrice =
        products.length > 0
          ? products.reduce((sum, p) => sum + parseFloat(p.price || 0), 0) /
            products.length
          : 0;
      const avgRating =
        reviews.length > 0
          ? reviews.reduce((sum, r) => sum + (r.overall_rating || 0), 0) /
            reviews.length
          : 0;
      const totalRevenue =
        sales.length > 0
          ? sales.reduce((sum, s) => sum + parseFloat(s.total_amount || 0), 0)
          : 0;
      const activeCustomers = customers.filter((c) => c.is_active).length;

      setStats({
        avgPrice: avgPrice.toFixed(2),
        avgRating: avgRating.toFixed(2),
        totalRevenue: totalRevenue,
        activeCustomers,
      });

      // Top products by revenue
      const productRevenue = {};
      sales.forEach((sale) => {
        const productName = sale.product_name || "Unknown";
        const amount = parseFloat(sale.total_amount || 0);
        productRevenue[productName] =
          (productRevenue[productName] || 0) + amount;
      });
      const topProds = Object.entries(productRevenue)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([name, revenue]) => ({ name, revenue }));

      setTopProducts(topProds);

      // Customer segments
      const segmentCounts = {};
      customers.forEach((customer) => {
        segmentCounts[customer.segment] =
          (segmentCounts[customer.segment] || 0) + 1;
      });
      const segments = Object.entries(segmentCounts)
        .sort((a, b) => b[1] - a[1])
        .map(([segment, count]) => ({ segment, count }));
      setSegmentData(segments);

      // Channel performance
      const channelRevenue = {};
      sales.forEach((sale) => {
        const channel = sale.channel || "Unknown";
        const amount = parseFloat(sale.total_amount || 0);
        channelRevenue[channel] = (channelRevenue[channel] || 0) + amount;
      });
      const channels = Object.entries(channelRevenue)
        .sort((a, b) => b[1] - a[1])
        .map(([channel, revenue]) => ({ channel, revenue }));

      setChannelData(channels);

      setLoading(false);
    } catch (err) {
      console.error("Error fetching advanced analytics:", err);
      setError("Failed to load advanced analytics. Please try again.");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdvancedAnalytics();
  }, []);

  return {
    loading,
    error,
    stats,
    topProducts,
    segmentData,
    channelData,
    refetch: fetchAdvancedAnalytics,
  };
}

export { useAdvancedAnalyticsData };
export default useAdvancedAnalyticsData;
