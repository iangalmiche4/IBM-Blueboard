/**
 * Utility functions for formatting data
 */

// Get settings from localStorage
const getSettings = () => {
  try {
    const saved = localStorage.getItem("ibm-blueboard-settings");
    return saved
      ? JSON.parse(saved)
      : { currency: "EUR", dateFormat: "DD/MM/YYYY" };
  } catch {
    return { currency: "EUR", dateFormat: "DD/MM/YYYY" };
  }
};

// Currency locale mapping
const getCurrencyLocale = (currency) => {
  const localeMap = {
    EUR: "fr-FR",
    USD: "en-US",
    GBP: "en-GB",
    JPY: "ja-JP",
  };
  return localeMap[currency] || "fr-FR";
};

/**
 * Format number as currency based on user settings
 */
export const formatCurrency = (value) => {
  const { currency } = getSettings();
  const locale = getCurrencyLocale(currency);

  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency: currency,
  }).format(value);
};

/**
 * Format number with thousands separator
 */
export const formatNumber = (value) => {
  return new Intl.NumberFormat("fr-FR").format(value);
};

/**
 * Format percentage value
 */
export const formatPercentage = (value, decimals = 1) => {
  return `${(value * 100).toFixed(decimals)}%`;
};

/**
 * Format date based on user settings
 */
export const formatDate = (date) => {
  const { dateFormat } = getSettings();
  const d = new Date(date);

  const day = String(d.getDate()).padStart(2, "0");
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const year = d.getFullYear();

  switch (dateFormat) {
    case "MM/DD/YYYY":
      return `${month}/${day}/${year}`;
    case "YYYY-MM-DD":
      return `${year}-${month}-${day}`;
    case "DD/MM/YYYY":
    default:
      return `${day}/${month}/${year}`;
  }
};
