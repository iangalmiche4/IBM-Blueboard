/**
 * Cached Analytics API
 */
import { createCachedAPI } from "./cacheUtils";
import config from "../../config/app.config";
import * as api from "../api/";

export const cachedAnalyticsAPI = {
  getDashboard: createCachedAPI(
    api.analyticsAPI.getDashboard,
    "analytics:dashboard",
    config.cache.ttl.dashboard,
  ),
  getSalesTrends: createCachedAPI(
    api.analyticsAPI.getSalesTrends,
    "analytics:sales-trends",
    config.cache.ttl.analytics,
  ),
  getTopProducts: createCachedAPI(
    api.analyticsAPI.getTopProducts,
    "analytics:top-products",
    config.cache.ttl.analytics,
  ),
  getCategoryDistribution: createCachedAPI(
    api.analyticsAPI.getCategoryDistribution,
    "analytics:category-dist",
    config.cache.ttl.analytics,
  ),
  getSatisfactionStats: createCachedAPI(
    api.analyticsAPI.getSatisfactionStats,
    "analytics:satisfaction",
    config.cache.ttl.analytics,
  ),
  getRegionalPerformance: createCachedAPI(
    api.analyticsAPI.getRegionalPerformance,
    "analytics:regional",
    config.cache.ttl.analytics,
  ),
};
