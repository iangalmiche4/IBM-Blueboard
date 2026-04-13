/**
 * Cached Products API
 */
import { createCachedAPI } from "./cacheUtils";
import config from "../../config/app.config";
import * as api from "../api/";

export const cachedProductsAPI = {
  getAll: createCachedAPI(
    api.productsAPI.getAll,
    "products:all",
    config.cache.ttl.products,
  ),
  getById: createCachedAPI(
    api.productsAPI.getById,
    "products:by-id",
    config.cache.ttl.products,
  ),
  getByCategory: createCachedAPI(
    api.productsAPI.getByCategory,
    "products:by-category",
    config.cache.ttl.products,
  ),
};
