/**
 * Analytics API endpoints
 */
import apiClient from "./client";
import { API_CONFIG } from "../../config/api";

export const analyticsAPI = {
  getDashboard: () => apiClient.get("/analytics/dashboard"),
  getSalesTrends: () => apiClient.get("/analytics/sales-trends"),
  getTopProducts: (limit = API_CONFIG.DEFAULT_LIMIT) =>
    apiClient.get(`/analytics/top-products?limit=${limit}`),
  getCategoryDistribution: () =>
    apiClient.get("/analytics/category-distribution"),
  getSatisfactionStats: () => apiClient.get("/analytics/satisfaction-stats"),
  getRegionalPerformance: () =>
    apiClient.get("/analytics/regional-performance"),
  getKPITrends: (periodDays = 30) =>
    apiClient.get(`/analytics/kpi-trends?period_days=${periodDays}`),
  getQuickStats: () => apiClient.get("/analytics/quick-stats"),
};
