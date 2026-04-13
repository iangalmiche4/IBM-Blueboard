/**
 * Settings Configuration
 * Defines all available settings sections and their options
 */

// Feature flags
const FEATURES = {
  LANGUAGE_SELECTOR: false, // Set to true when i18n is implemented
};

export const getSettingsConfig = (
  theme,
  settings,
  setTheme,
  handleChange,
  setSaved,
) => [
  {
    title: "Appearance",
    settings: [
      {
        id: "theme-select",
        label: "Theme",
        value: theme,
        onChange: (e) => {
          setTheme(e.target.value);
          setSaved(false);
        },
        options: [
          { value: "g10", text: "Light" },
          { value: "g100", text: "Dark" },
        ],
      },
      // Language selector - hidden until i18n is implemented
      ...(FEATURES.LANGUAGE_SELECTOR
        ? [
            {
              id: "language-select",
              label: "Language",
              value: settings.language,
              onChange: (e) => handleChange("language", e.target.value),
              options: [
                { value: "en", text: "English" },
                { value: "fr", text: "Français" },
                { value: "de", text: "Deutsch" },
                { value: "es", text: "Español" },
              ],
            },
          ]
        : []),
    ],
  },
  {
    title: "Regional",
    settings: [
      {
        id: "currency-select",
        label: "Currency",
        value: settings.currency,
        onChange: (e) => handleChange("currency", e.target.value),
        options: [
          { value: "EUR", text: "Euro (€)" },
          { value: "USD", text: "US Dollar ($)" },
          { value: "GBP", text: "British Pound (£)" },
          { value: "JPY", text: "Japanese Yen (¥)" },
        ],
      },
      {
        id: "date-format-select",
        label: "Date Format",
        value: settings.dateFormat,
        onChange: (e) => handleChange("dateFormat", e.target.value),
        options: [
          { value: "DD/MM/YYYY", text: "DD/MM/YYYY" },
          { value: "MM/DD/YYYY", text: "MM/DD/YYYY" },
          { value: "YYYY-MM-DD", text: "YYYY-MM-DD" },
        ],
      },
    ],
  },
  {
    title: "Export",
    settings: [
      {
        id: "export-format-select",
        label: "Default Export Format",
        value: settings.exportFormat,
        onChange: (e) => handleChange("exportFormat", e.target.value),
        options: [
          { value: "csv", text: "CSV" },
          { value: "xlsx", text: "Excel (XLSX)" },
          { value: "json", text: "JSON" },
          { value: "pdf", text: "PDF" },
        ],
      },
    ],
  },
];
