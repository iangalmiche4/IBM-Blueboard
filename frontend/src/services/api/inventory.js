/**
 * Inventory API endpoints
 */
import apiClient from "./client";
import { API_CONFIG } from "../../config/api";

export const inventoryAPI = {
  getAll: (skip = API_CONFIG.DEFAULT_SKIP, limit = API_CONFIG.DEFAULT_LIMIT) =>
    apiClient.get(`/inventory?skip=${skip}&limit=${limit}`),
  getById: (id) => apiClient.get(`/inventory/${id}`),
  getByProduct: (productId) =>
    apiClient.get(`/inventory/by-product/${productId}`),
  getByWarehouse: (warehouse) =>
    apiClient.get(`/inventory/by-warehouse/${warehouse}`),
  getLowStockAlerts: (threshold = 10) =>
    apiClient.get(`/inventory/low-stock?threshold=${threshold}`),
  getStats: () => apiClient.get("/inventory/stats"),
  getWithProducts: () => apiClient.get("/inventory/with-products"),
};
