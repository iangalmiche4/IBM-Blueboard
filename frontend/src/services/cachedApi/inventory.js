/**
 * Cached Inventory API
 */
import { createCachedAPI } from "./cacheUtils";
import config from "../../config/app.config";
import * as api from "../api/";

export const cachedInventoryAPI = {
  getAll: createCachedAPI(
    api.inventoryAPI.getAll,
    "inventory:all",
    config.cache.ttl.inventory,
  ),
  getById: createCachedAPI(
    api.inventoryAPI.getById,
    "inventory:by-id",
    config.cache.ttl.inventory,
  ),
  getByProduct: createCachedAPI(
    api.inventoryAPI.getByProduct,
    "inventory:by-product",
    config.cache.ttl.inventory,
  ),
  getByWarehouse: createCachedAPI(
    api.inventoryAPI.getByWarehouse,
    "inventory:by-warehouse",
    config.cache.ttl.inventory,
  ),
  getLowStockAlerts: createCachedAPI(
    api.inventoryAPI.getLowStockAlerts,
    "inventory:low-stock",
    config.cache.ttl.lowStockAlerts,
  ),
  getStats: createCachedAPI(
    api.inventoryAPI.getStats,
    "inventory:stats",
    config.cache.ttl.inventory,
  ),
  getWithProducts: createCachedAPI(
    api.inventoryAPI.getWithProducts,
    "inventory:with-products",
    config.cache.ttl.inventory,
  ),
};
