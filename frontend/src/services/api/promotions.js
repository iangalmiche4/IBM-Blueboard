/**
 * Promotions API endpoints
 */
import apiClient from "./client";
import { API_CONFIG } from "../../config/api";

export const promotionsAPI = {
  getAll: (skip = API_CONFIG.DEFAULT_SKIP, limit = API_CONFIG.DEFAULT_LIMIT) =>
    apiClient.get(`/promotions?skip=${skip}&limit=${limit}`),
  getById: (id) => apiClient.get(`/promotions/${id}`),
  getActive: () => apiClient.get("/promotions/active"),
  getByType: (type) => apiClient.get(`/promotions/by-type/${type}`),
  getStats: () => apiClient.get("/promotions/stats"),
  getROI: () => apiClient.get("/promotions/roi"),
  getWithSales: () => apiClient.get("/promotions/with-sales"),
};
