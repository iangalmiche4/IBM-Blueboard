/**
 * Cached Returns API
 */
import { createCachedAPI } from "./cacheUtils";
import config from "../../config/app.config";
import * as api from "../api/";

export const cachedReturnsAPI = {
  getAll: createCachedAPI(
    api.returnsAPI.getAll,
    "returns:all",
    config.cache.ttl.returns,
  ),
  getById: createCachedAPI(
    api.returnsAPI.getById,
    "returns:by-id",
    config.cache.ttl.returns,
  ),
  getByStatus: createCachedAPI(
    api.returnsAPI.getByStatus,
    "returns:by-status",
    config.cache.ttl.returns,
  ),
  getByCustomer: createCachedAPI(
    api.returnsAPI.getByCustomer,
    "returns:by-customer",
    config.cache.ttl.returns,
  ),
  getByProduct: createCachedAPI(
    api.returnsAPI.getByProduct,
    "returns:by-product",
    config.cache.ttl.returns,
  ),
  getStats: createCachedAPI(
    api.returnsAPI.getStats,
    "returns:stats",
    config.cache.ttl.returns,
  ),
  getReasonAnalysis: createCachedAPI(
    api.returnsAPI.getReasonAnalysis,
    "returns:reason-analysis",
    config.cache.ttl.returns,
  ),
  getProductReturnRates: createCachedAPI(
    api.returnsAPI.getProductReturnRates,
    "returns:product-rates",
    config.cache.ttl.returns,
  ),
  getWithDetails: createCachedAPI(
    api.returnsAPI.getWithDetails,
    "returns:with-details",
    config.cache.ttl.returns,
  ),
};
