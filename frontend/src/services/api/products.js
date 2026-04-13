/**
 * Products API endpoints
 */
import apiClient from "./client";
import { API_CONFIG } from "../../config/api";

export const productsAPI = {
  getAll: (
    skip = API_CONFIG.DEFAULT_SKIP,
    limit = API_CONFIG.DEFAULT_LIMIT,
    category = null,
  ) => {
    const params = new URLSearchParams({ skip, limit });
    if (category) params.append("category", category);
    return apiClient.get(`/products?${params}`);
  },
  getById: (id) => apiClient.get(`/products/${id}`),
  getByCategory: (category) => apiClient.get(`/products/category/${category}`),
};
