/**
 * Returns API endpoints
 */
import apiClient from "./client";
import { API_CONFIG } from "../../config/api";

export const returnsAPI = {
  getAll: (skip = API_CONFIG.DEFAULT_SKIP, limit = API_CONFIG.DEFAULT_LIMIT) =>
    apiClient.get(`/returns?skip=${skip}&limit=${limit}`),
  getById: (id) => apiClient.get(`/returns/${id}`),
  getByStatus: (status) => apiClient.get(`/returns/by-status/${status}`),
  getByCustomer: (customerId) =>
    apiClient.get(`/returns/by-customer/${customerId}`),
  getByProduct: (productId) =>
    apiClient.get(`/returns/by-product/${productId}`),
  getStats: () => apiClient.get("/returns/stats"),
  getReasonAnalysis: () => apiClient.get("/returns/reason-analysis"),
  getProductReturnRates: () => apiClient.get("/returns/product-rates"),
  getWithDetails: () => apiClient.get("/returns/with-details"),
};
