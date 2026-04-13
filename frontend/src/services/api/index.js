/**
 * API Services - Central export point
 * Import all API endpoints from their respective modules
 */
export { analyticsAPI } from "./analytics";
export { productsAPI } from "./products";
export { salesAPI } from "./sales";
export { satisfactionAPI } from "./satisfaction";
export { customersAPI } from "./customers";
export { inventoryAPI } from "./inventory";
export { promotionsAPI } from "./promotions";
export { returnsAPI } from "./returns";
export { systemAPI } from "./system";

// Export the axios client for direct use if needed
export { default as apiClient } from "./client";
