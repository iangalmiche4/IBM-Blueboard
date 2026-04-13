/**
 * Theme Store Module
 * Manages application theme (light/dark mode) with scroll preservation
 */
export class ThemeStore {
  constructor() {
    this.theme = localStorage.getItem("ibm-blueboard-theme") || "g10";
    this.listeners = new Set();
    this.tableStates = new Map(); // Store for preserving table pagination states
    this.applyTheme(this.theme);
  }

  /**
   * Save table pagination state
   * @param {string} tableId - Unique identifier for the table
   * @param {Object} state - State object containing currentPage and pageSize
   */
  saveTableState(tableId, state) {
    this.tableStates.set(tableId, state);
  }

  /**
   * Get saved table pagination state
   * @param {string} tableId - Unique identifier for the table
   * @returns {Object|undefined} Saved state or undefined if not found
   */
  getTableState(tableId) {
    return this.tableStates.get(tableId);
  }

  /**
   * Clear table state
   * @param {string} tableId - Unique identifier for the table
   */
  clearTableState(tableId) {
    this.tableStates.delete(tableId);
  }

  getTheme() {
    return this.theme;
  }

  setTheme(newTheme) {
    if (this.theme === newTheme) return;

    // Save scroll position from multiple possible scroll containers
    const rootElement = document.getElementById("root");
    const contentElement = document.querySelector(".app-content");
    const bodyElement = document.body;
    const htmlElement = document.documentElement;

    const scrollPositions = {
      root: rootElement?.scrollTop || 0,
      content: contentElement?.scrollTop || 0,
      body: bodyElement?.scrollTop || 0,
      html: htmlElement?.scrollTop || 0,
      window: window.scrollY || window.pageYOffset || 0,
    };

    this.theme = newTheme;
    localStorage.setItem("ibm-blueboard-theme", newTheme);

    // Apply theme
    this.applyTheme(newTheme);

    // Notify listeners
    this.notifyListeners();

    // Restore scroll position after React updates
    const restoreScroll = () => {
      const root = document.getElementById("root");
      const content = document.querySelector(".app-content");
      const body = document.body;
      const html = document.documentElement;

      if (root && scrollPositions.root > 0) {
        root.scrollTop = scrollPositions.root;
      }
      if (content && scrollPositions.content > 0) {
        content.scrollTop = scrollPositions.content;
      }
      if (body && scrollPositions.body > 0) {
        body.scrollTop = scrollPositions.body;
      }
      if (html && scrollPositions.html > 0) {
        html.scrollTop = scrollPositions.html;
      }
      if (scrollPositions.window > 0) {
        window.scrollTo(0, scrollPositions.window);
      }
    };

    requestAnimationFrame(restoreScroll);
    setTimeout(restoreScroll, 0);
    setTimeout(restoreScroll, 10);
    setTimeout(restoreScroll, 50);
    setTimeout(restoreScroll, 100);
  }

  applyTheme(theme) {
    document.documentElement.setAttribute("data-carbon-theme", theme);
    document.body.setAttribute("data-carbon-theme", theme);

    const bgColor = getComputedStyle(document.documentElement)
      .getPropertyValue("--cds-background")
      .trim();
    const textColor = getComputedStyle(document.documentElement)
      .getPropertyValue("--cds-text-primary")
      .trim();

    document.documentElement.style.setProperty(
      "background-color",
      bgColor,
      "important",
    );
    document.body.style.setProperty("background-color", bgColor, "important");
    document.body.style.setProperty("color", textColor, "important");

    const root = document.getElementById("root");
    if (root) {
      root.style.setProperty("background-color", bgColor, "important");
      root.style.setProperty("color", textColor, "important");
    }
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notifyListeners() {
    this.listeners.forEach((listener) => listener());
  }
}

// Export singleton instance
export const themeStore = new ThemeStore();
