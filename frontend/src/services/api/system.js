/**
 * System API endpoints
 */
import apiClient from "./client";

export const systemAPI = {
  getInfo: () => apiClient.get("/system/info"),
};
