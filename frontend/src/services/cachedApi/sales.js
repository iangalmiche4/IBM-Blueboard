/**
 * Cached Sales API
 */
import { createCachedAPI } from "./cacheUtils";
import config from "../../config/app.config";
import * as api from "../api/";

export const cachedSalesAPI = {
  getAll: createCachedAPI(
    api.salesAPI.getAll,
    "sales:all",
    config.cache.ttl.sales,
  ),
  getStats: createCachedAPI(
    api.salesAPI.getStats,
    "sales:stats",
    config.cache.ttl.sales,
  ),
  getByRegion: createCachedAPI(
    api.salesAPI.getByRegion,
    "sales:by-region",
    config.cache.ttl.sales,
  ),
  getTopProducts: createCachedAPI(
    api.salesAPI.getTopProducts,
    "sales:top-products",
    config.cache.ttl.sales,
  ),
};
