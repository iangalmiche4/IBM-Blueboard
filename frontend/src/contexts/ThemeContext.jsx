/**
 * Theme Context - Now uses centralized AppStore
 * This file is kept for backward compatibility
 * Import from AppStore instead: import { useTheme } from '../store/AppStore';
 */
export { useTheme } from "../store/AppStore";

export const ThemeProvider = ({ children }) => {
  return children;
};
