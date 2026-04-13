/**
 * Customers API endpoints
 */
import apiClient from "./client";
import { API_CONFIG } from "../../config/api";

export const customersAPI = {
  getAll: (
    skip = API_CONFIG.DEFAULT_SKIP,
    limit = API_CONFIG.DEFAULT_LIMIT,
    segment = null,
  ) => {
    const params = new URLSearchParams({ skip, limit });
    if (segment) params.append("segment", segment);
    return apiClient.get(`/customers?${params}`);
  },
  getById: (id) => apiClient.get(`/customers/${id}`),
  getSegmentDistribution: () =>
    apiClient.get("/customers/segments/distribution"),
};
