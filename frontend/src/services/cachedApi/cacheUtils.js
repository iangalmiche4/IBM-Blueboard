/**
 * Cache Utilities - Helper functions for cache management
 */
import config from "../../config/app.config";
import { appStore } from "../../store/AppStore";

/**
 * Create a cached version of an API function
 * @param {Function} apiFunc - The API function to cache
 * @param {string} cacheKey - The cache key prefix
 * @param {number} ttl - Time to live in milliseconds
 * @returns {Function} Cached API function
 */
export const createCachedAPI = (apiFunc, cacheKey, ttl) => {
  return async (...args) => {
    // If cache is disabled, call API directly
    if (!config.cache.enabled) {
      return apiFunc(...args);
    }

    // Create unique cache key based on function and arguments
    const key = `${cacheKey}:${JSON.stringify(args)}`;

    // Try to get from cache
    const cached = appStore.getCached(key);
    if (cached) {
      if (config.features.enableDebugMode) {
        console.log(`[Cache HIT] ${key}`);
      }
      return { data: cached, fromCache: true };
    }

    // Cache miss - fetch from API
    if (config.features.enableDebugMode) {
      console.log(`[Cache MISS] ${key}`);
    }
    const response = await apiFunc(...args);

    // Store in cache
    appStore.setCache(key, response.data, ttl);

    return { ...response, fromCache: false };
  };
};

/**
 * Clear all API cache
 */
export const clearAllCache = () => {
  appStore.clearCache();
  console.log("[Cache] All cache cleared");
};

/**
 * Clear cache for specific API group
 * @param {string} prefix - Cache key prefix (e.g., 'analytics', 'products')
 */
export const clearCacheByPrefix = (prefix) => {
  const cache = appStore.cache;
  const keysToDelete = [];

  cache.forEach((_, key) => {
    if (key.startsWith(prefix)) {
      keysToDelete.push(key);
    }
  });

  keysToDelete.forEach((key) => appStore.clearCache(key));
  if (config.features.enableDebugMode) {
    console.log(
      `[Cache] Cleared ${keysToDelete.length} entries for prefix: ${prefix}`,
    );
  }
};

/**
 * Get cache statistics
 */
export const getCacheStats = () => {
  return appStore.getCacheStats();
};
