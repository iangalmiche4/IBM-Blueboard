/**
 * Cached Customers API
 */
import { createCachedAPI } from "./cacheUtils";
import config from "../../config/app.config";
import * as api from "../api/";

export const cachedCustomersAPI = {
  getAll: createCachedAPI(
    api.customersAPI.getAll,
    "customers:all",
    config.cache.ttl.customers,
  ),
  getById: createCachedAPI(
    api.customersAPI.getById,
    "customers:by-id",
    config.cache.ttl.customers,
  ),
  getSegmentDistribution: createCachedAPI(
    api.customersAPI.getSegmentDistribution,
    "customers:segments",
    config.cache.ttl.customers,
  ),
};
