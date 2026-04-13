/**
 * Configuration Loader
 * Loads configuration from config.txt file
 * Priority: ENV VAR > config.txt > default value
 */

let fileConfig = {};

/**
 * Load configuration from config.txt
 * This runs synchronously during module initialization
 */
try {
  // In production build, config.txt should be in public folder
  const configUrl = "/config.txt";

  // Use XMLHttpRequest for synchronous loading during initialization
  const xhr = new XMLHttpRequest();
  xhr.open("GET", configUrl, false); // false = synchronous
  xhr.send(null);

  if (xhr.status === 200) {
    const lines = xhr.responseText.split("\n");
    lines.forEach((line) => {
      line = line.trim();
      // Skip comments and empty lines
      if (line && !line.startsWith("#")) {
        const [key, ...valueParts] = line.split("=");
        if (key && valueParts.length > 0) {
          const value = valueParts.join("=").trim();
          fileConfig[key.trim()] = value;
        }
      }
    });
    console.log("[Config] Loaded configuration from config.txt");
  }
} catch (error) {
  console.warn(
    "[Config] Could not load config.txt, using defaults:",
    error.message,
  );
}

/**
 * Get configuration value with priority: ENV > file > default
 * @param {string} envKey - Environment variable key (e.g., 'VITE_API_URL')
 * @param {string} fileKey - Config file key (e.g., 'API_URL')
 * @param {any} defaultValue - Default value if not found
 * @returns {any} Configuration value
 */
export const getConfig = (envKey, fileKey, defaultValue) => {
  // Priority 1: Environment variable
  if (import.meta.env[envKey] !== undefined) {
    return import.meta.env[envKey];
  }

  // Priority 2: Config file
  if (fileConfig[fileKey] !== undefined) {
    const value = fileConfig[fileKey];

    // Convert string booleans to actual booleans
    if (value === "true") return true;
    if (value === "false") return false;

    // Convert string numbers to actual numbers
    if (!isNaN(value) && value !== "") {
      return Number(value);
    }

    return value;
  }

  // Priority 3: Default value
  return defaultValue;
};

/**
 * Get all loaded file config (for debugging)
 */
export const getFileConfig = () => fileConfig;
