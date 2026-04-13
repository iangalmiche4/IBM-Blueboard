/**
 * Cached Satisfaction API
 */
import { createCachedAPI } from "./cacheUtils";
import config from "../../config/app.config";
import * as api from "../api/";

export const cachedSatisfactionAPI = {
  getAll: createCachedAPI(
    api.satisfactionAPI.getAll,
    "satisfaction:all",
    config.cache.ttl.satisfaction,
  ),
  getStats: createCachedAPI(
    api.satisfactionAPI.getStats,
    "satisfaction:stats",
    config.cache.ttl.satisfaction,
  ),
  getByProduct: createCachedAPI(
    api.satisfactionAPI.getByProduct,
    "satisfaction:by-product",
    config.cache.ttl.satisfaction,
  ),
  getAverage: createCachedAPI(
    api.satisfactionAPI.getAverage,
    "satisfaction:average",
    config.cache.ttl.satisfaction,
  ),
};
