import { useEffect, useState } from "react";
import { Reset, Save } from "@carbon/icons-react";
import {
  Accordion,
  Button,
  Column,
  Grid,
  InlineNotification,
} from "@carbon/react";
import {
  PageHeader,
  SettingSection,
  SettingSelect,
  SystemInfoSection,
} from "../components/ui";
import { getSettingsConfig } from "../config/settingsConfig";
import { useSettings } from "../contexts/SettingsContext";
import { useTheme } from "../contexts/ThemeContext";

function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const { settings, updateSetting, resetSettings } = useSettings();

  const [saved, setSaved] = useState(false);
  const [tempSettings, setTempSettings] = useState(settings);
  const [tempTheme, setTempTheme] = useState(theme);
  const [hasChanges, setHasChanges] = useState(false);

  // Sync temp settings with actual settings on mount
  useEffect(() => {
    setTempSettings(settings);
    setTempTheme(theme);
  }, [settings, theme]);

  const handleChange = (key, value) => {
    setTempSettings((prev) => ({ ...prev, [key]: value }));
    setHasChanges(true);
    setSaved(false);
  };

  const handleThemeChange = (newTheme) => {
    setTempTheme(newTheme);
    setHasChanges(true);
    setSaved(false);
  };

  const handleSave = () => {
    // Apply all changes to context (which saves to localStorage)
    Object.keys(tempSettings).forEach((key) => {
      if (tempSettings[key] !== settings[key]) {
        updateSetting(key, tempSettings[key]);
      }
    });

    if (tempTheme !== theme) {
      setTheme(tempTheme);
    }

    setHasChanges(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleReset = () => {
    resetSettings();
    setTheme("g10");
    setTempSettings(settings);
    setTempTheme("g10");
    setHasChanges(false);
    setSaved(false);
  };

  const settingsConfig = getSettingsConfig(
    tempTheme,
    tempSettings,
    handleThemeChange,
    handleChange,
    setSaved,
  );

  return (
    <div className="page-container">
      <PageHeader
        title="Settings"
        subtitle="Configure your IBM Blueboard preferences"
      />

      {saved && (
        <Grid narrow>
          <Column sm={4} md={8} lg={16}>
            <InlineNotification
              kind="success"
              title="Settings saved"
              subtitle="Your preferences have been updated successfully"
              lowContrast
            />
          </Column>
        </Grid>
      )}

      <Grid narrow>
        <Column sm={4} md={8} lg={16}>
          <Accordion>
            {settingsConfig.map((section) => (
              <SettingSection key={section.title} title={section.title}>
                {section.settings.map((setting) => (
                  <SettingSelect
                    key={setting.id}
                    id={setting.id}
                    label={setting.label}
                    value={setting.value}
                    onChange={setting.onChange}
                    options={setting.options}
                  />
                ))}
              </SettingSection>
            ))}
          </Accordion>
        </Column>
      </Grid>

      {/* Action Buttons */}
      <Grid narrow className="mt-2">
        <Column sm={4} md={8} lg={16}>
          <div className="flex-align-center flex-gap-1">
            <Button
              kind="primary"
              renderIcon={Save}
              onClick={handleSave}
              disabled={!hasChanges}
            >
              Save Settings
            </Button>
            <Button kind="secondary" renderIcon={Reset} onClick={handleReset}>
              Reset to Defaults
            </Button>
            {hasChanges && (
              <span className="text-secondary text-small">
                You have unsaved changes
              </span>
            )}
          </div>
        </Column>
      </Grid>

      {/* System Info */}
      <Grid narrow className="mt-3">
        <Column sm={4} md={8} lg={16}>
          <SystemInfoSection />
        </Column>
      </Grid>
    </div>
  );
}

export default SettingsPage;
