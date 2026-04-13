/**
 * Settings Store Module
 * Manages user preferences and application settings
 */
import config from "../config/app.config";

export class SettingsStore {
  constructor() {
    this.settings = this.loadSettings();
    this.listeners = new Set();
  }

  loadSettings() {
    const defaultSettings = {
      // Display settings
      notifications: config.features.enableNotifications,
      autoRefresh: config.features.enableAutoRefresh,
      refreshInterval: config.defaults.refreshInterval,
      compactMode: false,
      showAnimations: config.features.enableAnimations,
      // Localization settings
      language: config.defaults.language,
      currency: config.defaults.currency,
      dateFormat: config.defaults.dateFormat,
      // Export settings
      exportFormat: config.defaults.exportFormat,
    };

    try {
      const saved = localStorage.getItem("ibm-blueboard-settings");
      return saved
        ? { ...defaultSettings, ...JSON.parse(saved) }
        : defaultSettings;
    } catch (error) {
      console.error("Error loading settings:", error);
      return defaultSettings;
    }
  }

  getSettings() {
    return this.settings;
  }

  updateSetting(key, value) {
    this.settings = { ...this.settings, [key]: value };
    localStorage.setItem(
      "ibm-blueboard-settings",
      JSON.stringify(this.settings),
    );
    this.notifyListeners();
  }

  updateSettings(newSettings) {
    this.settings = { ...this.settings, ...newSettings };
    localStorage.setItem(
      "ibm-blueboard-settings",
      JSON.stringify(this.settings),
    );
    this.notifyListeners();
  }

  resetSettings() {
    this.settings = this.loadSettings();
    localStorage.removeItem("ibm-blueboard-settings");
    this.notifyListeners();
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notifyListeners() {
    this.listeners.forEach((listener) => listener());
  }
}
