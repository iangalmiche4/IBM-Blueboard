/**
 * Application Configuration
 * Priority: ENV VAR > config.txt > default value
 */
import { getConfig } from "./configLoader";

const config = {
  // API Configuration
  api: {
    baseURL: getConfig(
      "VITE_API_URL",
      "API_URL",
      "http://localhost:8000/api/v1",
    ),
    timeout: getConfig("VITE_API_TIMEOUT", "API_TIMEOUT", 30000),
  },

  // Cache Configuration
  cache: {
    enabled: getConfig("VITE_ENABLE_CACHE", "ENABLE_CACHE", true),
    defaultTTL: 5 * 60 * 1000,
    ttl: {
      dashboard: getConfig(
        "VITE_CACHE_TTL_DASHBOARD",
        "CACHE_TTL_DASHBOARD",
        120000,
      ),
      analytics: getConfig(
        "VITE_CACHE_TTL_ANALYTICS",
        "CACHE_TTL_ANALYTICS",
        300000,
      ),
      products: getConfig(
        "VITE_CACHE_TTL_PRODUCTS",
        "CACHE_TTL_PRODUCTS",
        600000,
      ),
      inventory: getConfig(
        "VITE_CACHE_TTL_INVENTORY",
        "CACHE_TTL_INVENTORY",
        120000,
      ),
      lowStockAlerts: getConfig(
        "VITE_CACHE_TTL_LOW_STOCK",
        "CACHE_TTL_LOW_STOCK",
        60000,
      ),
      sales: getConfig("VITE_CACHE_TTL_SALES", "CACHE_TTL_SALES", 180000),
      customers: getConfig(
        "VITE_CACHE_TTL_CUSTOMERS",
        "CACHE_TTL_CUSTOMERS",
        600000,
      ),
      promotions: getConfig(
        "VITE_CACHE_TTL_PROMOTIONS",
        "CACHE_TTL_PROMOTIONS",
        300000,
      ),
      returns: getConfig("VITE_CACHE_TTL_RETURNS", "CACHE_TTL_RETURNS", 300000),
      satisfaction: getConfig(
        "VITE_CACHE_TTL_SATISFACTION",
        "CACHE_TTL_SATISFACTION",
        300000,
      ),
    },
  },

  // Feature Flags
  features: {
    enableNotifications: getConfig(
      "VITE_ENABLE_NOTIFICATIONS",
      "ENABLE_NOTIFICATIONS",
      true,
    ),
    enableAutoRefresh: getConfig(
      "VITE_ENABLE_AUTO_REFRESH",
      "ENABLE_AUTO_REFRESH",
      true,
    ),
    enableAnimations: getConfig(
      "VITE_ENABLE_ANIMATIONS",
      "ENABLE_ANIMATIONS",
      true,
    ),
    enableExport: getConfig("VITE_ENABLE_EXPORT", "ENABLE_EXPORT", true),
    enableDebugMode: import.meta.env.DEV,
  },

  // Default Settings
  defaults: {
    language: getConfig("VITE_DEFAULT_LANGUAGE", "DEFAULT_LANGUAGE", "en"),
    currency: getConfig("VITE_DEFAULT_CURRENCY", "DEFAULT_CURRENCY", "EUR"),
    dateFormat: getConfig(
      "VITE_DEFAULT_DATE_FORMAT",
      "DEFAULT_DATE_FORMAT",
      "DD/MM/YYYY",
    ),
    exportFormat: getConfig(
      "VITE_DEFAULT_EXPORT_FORMAT",
      "DEFAULT_EXPORT_FORMAT",
      "csv",
    ),
    refreshInterval: getConfig(
      "VITE_DEFAULT_REFRESH_INTERVAL",
      "DEFAULT_REFRESH_INTERVAL",
      30,
    ),
  },
};

export default config;
