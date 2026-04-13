/**
 * Application Store
 * Centralized state management using modular stores
 */
import { useSyncExternalStore } from "react";
import { CacheStore } from "./CacheStore";
import { SettingsStore } from "./SettingsStore";
import { ThemeStore } from "./ThemeStore";

/**
 * Main Application Store
 * Combines all sub-stores into a single interface
 */
class AppStore {
  constructor() {
    // Initialize sub-stores
    this.themeStore = new ThemeStore();
    this.settingsStore = new SettingsStore();
    this.cacheStore = new CacheStore();

    // Unified listeners
    this.listeners = new Set();

    // Subscribe to sub-store changes
    this.themeStore.subscribe(() => this.notifyListeners());
    this.settingsStore.subscribe(() => this.notifyListeners());
  }

  // ==================== THEME METHODS ====================

  getTheme() {
    return this.themeStore.getTheme();
  }

  setTheme(newTheme) {
    this.themeStore.setTheme(newTheme);
  }

  // ==================== SETTINGS METHODS ====================

  getSettings() {
    return this.settingsStore.getSettings();
  }

  updateSetting(key, value) {
    this.settingsStore.updateSetting(key, value);
  }

  updateSettings(newSettings) {
    this.settingsStore.updateSettings(newSettings);
  }

  resetSettings() {
    this.settingsStore.resetSettings();
  }

  // ==================== CACHE METHODS ====================

  getCached(key) {
    return this.cacheStore.getCached(key);
  }

  setCache(key, data, ttl) {
    this.cacheStore.setCache(key, data, ttl);
  }

  clearCache(key) {
    this.cacheStore.clearCache(key);
  }

  getCacheStats() {
    return this.cacheStore.getCacheStats();
  }

  // Direct access to cache Map for advanced operations
  get cache() {
    return this.cacheStore.cache;
  }

  // ==================== SUBSCRIPTION MANAGEMENT ====================

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notifyListeners() {
    this.listeners.forEach((listener) => listener());
  }

  // ==================== UTILITY METHODS ====================

  /**
   * Get all store state (for debugging)
   */
  getState() {
    return {
      theme: this.getTheme(),
      settings: this.getSettings(),
      cacheStats: this.getCacheStats(),
    };
  }

  /**
   * Clear all stored data
   */
  clearAll() {
    localStorage.removeItem("ibm-blueboard-theme");
    localStorage.removeItem("ibm-blueboard-settings");
    this.cacheStore.clearCache();
    this.themeStore.theme = "g10";
    this.themeStore.applyTheme("g10");
    this.settingsStore.settings = this.settingsStore.loadSettings();
    this.notifyListeners();
  }
}

// Create singleton instance
const appStore = new AppStore();

// Export store instance for direct access
export { appStore };

// ==================== REACT HOOKS ====================

/**
 * Hook to use theme from store
 */
export const useTheme = () => {
  const theme = useSyncExternalStore(
    (callback) => appStore.subscribe(callback),
    () => appStore.getTheme(),
    () => appStore.getTheme(),
  );

  return {
    theme,
    setTheme: (newTheme) => appStore.setTheme(newTheme),
  };
};

/**
 * Hook to use settings from store
 */
export const useSettings = () => {
  const settings = useSyncExternalStore(
    (callback) => appStore.subscribe(callback),
    () => appStore.getSettings(),
    () => appStore.getSettings(),
  );

  return {
    settings,
    updateSetting: (key, value) => appStore.updateSetting(key, value),
    updateSettings: (newSettings) => appStore.updateSettings(newSettings),
    resetSettings: () => appStore.resetSettings(),
  };
};

/**
 * Hook to use API cache
 */
export const useCache = () => {
  return {
    getCached: (key) => appStore.getCached(key),
    setCache: (key, data, ttl) => appStore.setCache(key, data, ttl),
    clearCache: (key) => appStore.clearCache(key),
    getCacheStats: () => appStore.getCacheStats(),
  };
};

/**
 * Hook to get entire store state (for debugging)
 */
export const useStore = () => {
  const state = useSyncExternalStore(
    (callback) => appStore.subscribe(callback),
    () => appStore.getState(),
    () => appStore.getState(),
  );

  return {
    ...state,
    clearAll: () => appStore.clearAll(),
  };
};
