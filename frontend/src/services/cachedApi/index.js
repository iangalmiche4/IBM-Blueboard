/**
 * Cached API - Central export point
 * Provides cached versions of all API endpoints organized by domain
 */

// Export all cached API modules
export { cachedAnalyticsAPI } from "./analytics";
export { cachedProductsAPI } from "./products";
export { cachedSalesAPI } from "./sales";
export { cachedSatisfactionAPI } from "./satisfaction";
export { cachedCustomersAPI } from "./customers";
export { cachedInventoryAPI } from "./inventory";
export { cachedPromotionsAPI } from "./promotions";
export { cachedReturnsAPI } from "./returns";
export { cachedSystemAPI } from "./system";

// Export cache utilities
export { clearAllCache, clearCacheByPrefix, getCacheStats } from "./cacheUtils";
