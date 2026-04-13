# Cache System

## Overview

IBM Blueboard uses a domain-driven cache system with configurable TTL per domain. Cache is **enabled by default**.

## Configuration

### Runtime Configuration (Recommended)

Edit `frontend/public/config.txt` to enable/disable cache without rebuilding:

```bash
# frontend/public/config.txt
ENABLE_CACHE=true
```

This file is loaded at runtime and takes precedence over environment variables.

### Build-time Configuration

Alternatively, use environment variables (requires rebuild):

```bash
# .env or .env.local
VITE_ENABLE_CACHE=true
```

### TTL Configuration

Cache TTL (Time To Live) is configured in `src/config/app.config.js`:

```javascript
cache: {
  enabled: true,  // Can be overridden by config.txt or env var
  ttl: {
    dashboard: 120000,      // 2 min
    analytics: 300000,      // 5 min
    products: 600000,       // 10 min
    inventory: 120000,      // 2 min
    lowStockAlerts: 60000,  // 1 min (critical)
    sales: 180000,          // 3 min
    customers: 600000,      // 10 min
    promotions: 300000,     // 5 min
    returns: 300000,        // 5 min
    satisfaction: 300000,   // 5 min
  }
}
```

**Configuration Priority:**

1. `public/config.txt` (highest - runtime)
2. Environment variables (`.env`)
3. Default values in `app.config.js` (lowest)

## Usage

### With Cache (Recommended for GET)

```javascript
import { cachedAnalyticsAPI } from "../services/cachedApi/";

const response = await cachedAnalyticsAPI.getDashboard();
console.log(response.fromCache); // true if from cache
```

### Without Cache (For mutations or real-time)

```javascript
import { apiClient } from "../services/api/";

const response = await apiClient.get("/analytics/dashboard");
```

## Cache Management

```javascript
import {
  clearAllCache,
  clearCacheByPrefix,
  getCacheStats,
} from "../services/cachedApi/";

// Clear all cache
clearAllCache();

// Clear specific domain
clearCacheByPrefix("inventory");

// Get cache statistics
const stats = getCacheStats();
```

## Best Practices

1. **Use cachedAPI** for data that changes infrequently
2. **Use direct API** for real-time data or mutations (POST, PUT, DELETE)
3. **Clear cache** after mutations that affect cached data
4. **Adjust TTL** based on data change frequency

## Example

```javascript
import { cachedInventoryAPI, clearCacheByPrefix } from "../services/cachedApi/";
import { apiClient } from "../services/api/";

// Load data (with cache)
const inventory = await cachedInventoryAPI.getWithProducts();

// Update data (without cache)
await apiClient.put(`/inventory/${id}`, data);

// Clear cache after update
clearCacheByPrefix("inventory");

// Reload fresh data
const updated = await cachedInventoryAPI.getWithProducts();
```

## Disable Cache

### Method 1: Runtime (No rebuild required)

```bash
# Edit frontend/public/config.txt
ENABLE_CACHE=false
```

### Method 2: Environment variable (Requires rebuild)

```bash
# .env
VITE_ENABLE_CACHE=false
```

### Method 3: Per call

Use direct API instead of cachedAPI:

```javascript
import { apiClient } from "../services/api/";
const response = await apiClient.get("/analytics/dashboard");
```

## Debug

Cache logs are enabled in development mode:

```
[Cache HIT] analytics:dashboard:[]
[Cache MISS] products:all:[]
[Cache] Cleared 5 entries for prefix: inventory
```
