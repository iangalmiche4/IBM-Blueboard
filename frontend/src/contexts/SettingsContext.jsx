/**
 * Settings Context - Now uses centralized AppStore
 * This file is kept for backward compatibility
 * Import from AppStore instead: import { useSettings } from '../store/AppStore';
 */
export { useSettings } from "../store/AppStore";

export function SettingsProvider({ children }) {
  return children;
}
