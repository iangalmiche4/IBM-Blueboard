/**
 * Cached Promotions API
 */
import { createCachedAPI } from "./cacheUtils";
import config from "../../config/app.config";
import * as api from "../api/";

export const cachedPromotionsAPI = {
  getAll: createCachedAPI(
    api.promotionsAPI.getAll,
    "promotions:all",
    config.cache.ttl.promotions,
  ),
  getById: createCachedAPI(
    api.promotionsAPI.getById,
    "promotions:by-id",
    config.cache.ttl.promotions,
  ),
  getActive: createCachedAPI(
    api.promotionsAPI.getActive,
    "promotions:active",
    config.cache.ttl.promotions,
  ),
  getByType: createCachedAPI(
    api.promotionsAPI.getByType,
    "promotions:by-type",
    config.cache.ttl.promotions,
  ),
  getStats: createCachedAPI(
    api.promotionsAPI.getStats,
    "promotions:stats",
    config.cache.ttl.promotions,
  ),
  getROI: createCachedAPI(
    api.promotionsAPI.getROI,
    "promotions:roi",
    config.cache.ttl.promotions,
  ),
  getWithSales: createCachedAPI(
    api.promotionsAPI.getWithSales,
    "promotions:with-sales",
    config.cache.ttl.promotions,
  ),
};
