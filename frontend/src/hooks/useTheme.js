/**
 * useTheme Hook
 * Provides easy access to theme state and actions
 */
import { useSyncExternalStore } from "react";
import { themeStore } from "../store/ThemeStore";

export function useTheme() {
  const theme = useSyncExternalStore(
    (callback) => themeStore.subscribe(callback),
    () => themeStore.getTheme(),
  );

  const setTheme = (newTheme) => {
    themeStore.setTheme(newTheme);
  };

  const toggleTheme = () => {
    const newTheme = theme === "g10" ? "g100" : "g10";
    themeStore.setTheme(newTheme);
  };

  return {
    theme,
    setTheme,
    toggleTheme,
    isDark: theme === "g100",
    isLight: theme === "g10",
  };
}
