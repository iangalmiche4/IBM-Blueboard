/**
 * Cached System API
 * Note: System info should not be cached
 */
import * as api from "../api/";

export const cachedSystemAPI = {
  getInfo: api.systemAPI.getInfo, // No cache for system info
};
