import { useEffect, useState } from "react";
import { API_CONFIG } from "../config/api";
import { apiClient } from "../services/api/";

function useDashboardData() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [kpis, setKpis] = useState(null);
  const [salesTrends, setSalesTrends] = useState([]);
  const [kpiTrends, setKpiTrends] = useState(null);
  const [quickStats, setQuickStats] = useState(null);
  const [categoryDistribution, setCategoryDistribution] = useState([]);
  const [channelPerformance, setChannelPerformance] = useState([]);
  const [regionDistribution, setRegionDistribution] = useState([]);
  const [promotionRoi, setPromotionRoi] = useState([]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all data in parallel
      const [
        kpiResponse,
        trendsResponse,
        kpiTrendsResponse,
        quickStatsResponse,
        salesResponse,
        roiResponse,
      ] = await Promise.all([
        apiClient.get("/analytics/dashboard"),
        apiClient.get("/analytics/sales-trends"),
        apiClient.get("/analytics/kpi-trends"),
        apiClient.get("/analytics/quick-stats"),
        apiClient.get(`/sales?limit=${API_CONFIG.DEFAULT_LIMIT}`),
        apiClient.get("/promotions/roi"),
      ]);

      // Set KPIs
      setKpis(kpiResponse.data.kpis || kpiResponse.data);

      // Set KPI trends
      setKpiTrends(kpiTrendsResponse.data);

      // Set quick stats
      setQuickStats(quickStatsResponse.data);

      // ---  ROI data processing ---
      if (roiResponse.data && Array.isArray(roiResponse.data)) {
        const roiMap = {};

        roiResponse.data.forEach((item) => {
          const label = item.promo_type || "Unknown";
          roiMap[label] = Number(parseFloat(item.roi_percentage || 0).toFixed(2));
        });

        const formattedRoi = Object.entries(roiMap)
          .map(([label, value]) => ({ label, value }))
          .sort((a, b) => b.value - a.value);

        setPromotionRoi(formattedRoi);
      }

      // Handle sales trends
      let trendsData = trendsResponse.data;
      if (!Array.isArray(trendsData)) {
        trendsData = trendsData.trends || [];
      }

      const formattedTrends = trendsData.map((item) => ({
        group: "Revenue",
        date: item.month || item.date,
        value: item.revenue || item.value || 0,
      }));
      setSalesTrends(formattedTrends);

      // Process sales data for additional charts
      const salesData = Array.isArray(salesResponse.data)
        ? salesResponse.data
        : salesResponse.data.sales || [];

      // Category distribution (for pie chart)
      const categoryMap = {};
      salesData.forEach((sale) => {
        const category = sale.category || "Other";
        categoryMap[category] =
          (categoryMap[category] || 0) + parseFloat(sale.total_amount || 0);
      });
      const categoryData = Object.entries(categoryMap)
        .map(([label, value]) => ({ label, value }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 6); // Top 6 categories
      setCategoryDistribution(categoryData);

      // Channel performance (for bar chart)
      const channelMap = {};
      salesData.forEach((sale) => {
        const channel = sale.channel || "Unknown";
        channelMap[channel] =
          (channelMap[channel] || 0) + parseFloat(sale.total_amount || 0);
      });
      const channelData = Object.entries(channelMap)
        .map(([label, value]) => ({ label, value }))
        .sort((a, b) => b.value - a.value);
      setChannelPerformance(channelData);

      // Region distribution (for pie chart)
      const regionMap = {};
      salesData.forEach((sale) => {
        const region = sale.region || "Unknown";
        regionMap[region] =
          (regionMap[region] || 0) + parseFloat(sale.total_amount || 0);
      });
      const regionData = Object.entries(regionMap)
        .map(([region, value]) => ({ group: region, value }))
        .sort((a, b) => a.group.localeCompare(b.group));
      setRegionDistribution(regionData);

      setLoading(false);
    } catch (err) {
      console.error("Error fetching dashboard data:", err);
      setError("Failed to load dashboard data. Please try again.");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return {
    loading,
    error,
    kpis,
    salesTrends,
    kpiTrends,
    quickStats,
    categoryDistribution,
    channelPerformance,
    regionDistribution,
    promotionRoi,
    refetch: fetchDashboardData,
  };
}

export { useDashboardData };
export default useDashboardData;
