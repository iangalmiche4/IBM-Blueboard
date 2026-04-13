/**
 * Sales API endpoints
 */
import apiClient from "./client";
import { API_CONFIG } from "../../config/api";

export const salesAPI = {
  getAll: (skip = API_CONFIG.DEFAULT_SKIP, limit = API_CONFIG.DEFAULT_LIMIT) =>
    apiClient.get(`/sales?skip=${skip}&limit=${limit}`),
  getStats: () => apiClient.get("/sales/stats"),
  getByRegion: () => apiClient.get("/sales/by-region"),
  getTopProducts: (limit = 10) =>
    apiClient.get(`/sales/top-products?limit=${limit}`),
};
