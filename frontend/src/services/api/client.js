/**
 * API Client - Axios instance configuration
 */
import axios from "axios";
import config from "../../config/app.config";

const apiClient = axios.create({
  baseURL: config.api.baseURL,
  timeout: config.api.timeout,
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
