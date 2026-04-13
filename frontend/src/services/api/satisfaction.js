/**
 * Satisfaction API endpoints
 */
import apiClient from "./client";
import { API_CONFIG } from "../../config/api";

export const satisfactionAPI = {
  getAll: (skip = API_CONFIG.DEFAULT_SKIP, limit = API_CONFIG.DEFAULT_LIMIT) =>
    apiClient.get(`/satisfaction?skip=${skip}&limit=${limit}`),
  getStats: () => apiClient.get("/satisfaction/stats"),
  getByProduct: (productId) =>
    apiClient.get(`/satisfaction/by-product/${productId}`),
  getAverage: () => apiClient.get("/satisfaction/average"),
};
