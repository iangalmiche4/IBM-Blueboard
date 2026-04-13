/**
 * Cache Store Module
 * Manages API response caching with TTL support
 */
import config from "../config/app.config";

export class CacheStore {
  constructor() {
    this.cache = new Map();
    this.cacheTTL = config.cache.defaultTTL;
  }

  /**
   * Get cached data for a key
   * @param {string} key - Cache key
   * @returns {any|null} Cached data or null if expired/not found
   */
  getCached(key) {
    const cached = this.cache.get(key);
    if (!cached) return null;

    const now = Date.now();
    if (now - cached.timestamp > cached.ttl) {
      this.cache.delete(key);
      return null;
    }

    return cached.data;
  }

  /**
   * Set cached data for a key
   * @param {string} key - Cache key
   * @param {any} data - Data to cache
   * @param {number} ttl - Time to live in milliseconds (optional)
   */
  setCache(key, data, ttl = this.cacheTTL) {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl,
    });
  }

  /**
   * Clear specific cache key or all cache
   * @param {string} key - Cache key (optional, clears all if not provided)
   */
  clearCache(key = null) {
    if (key) {
      this.cache.delete(key);
    } else {
      this.cache.clear();
    }
  }

  /**
   * Get cache statistics
   * @returns {object} Cache stats
   */
  getCacheStats() {
    const now = Date.now();
    let validEntries = 0;
    let expiredEntries = 0;

    this.cache.forEach((value) => {
      if (now - value.timestamp > value.ttl) {
        expiredEntries++;
      } else {
        validEntries++;
      }
    });

    return {
      total: this.cache.size,
      valid: validEntries,
      expired: expiredEntries,
    };
  }
}
