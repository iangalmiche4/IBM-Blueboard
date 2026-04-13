/**
 * useFetchData Hook
 * Generic hook for fetching data with loading and error states
 */
import { useCallback, useEffect, useState } from "react";

/**
 * @param {Function} fetchFunction - Async function that fetches data
 * @param {Array} dependencies - Dependencies array for useEffect
 * @param {Object} options - Configuration options
 * @param {boolean} options.immediate - Whether to fetch immediately (default: true)
 * @param {Function} options.onSuccess - Callback on successful fetch
 * @param {Function} options.onError - Callback on error
 */
export function useFetchData(fetchFunction, dependencies = [], options = {}) {
  const { immediate = true, onSuccess, onError } = options;

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(immediate);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetchFunction();
      const fetchedData = response.data;

      setData(fetchedData);

      if (onSuccess) {
        onSuccess(fetchedData);
      }

      return fetchedData;
    } catch (err) {
      console.error("Error fetching data:", err);
      const errorMessage =
        err.response?.data?.detail || err.message || "Failed to fetch data";
      setError(errorMessage);

      if (onError) {
        onError(err);
      }

      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchFunction, onSuccess, onError]);

  useEffect(() => {
    if (immediate) {
      fetchData();
    }
  }, dependencies);

  const refetch = useCallback(() => {
    return fetchData();
  }, [fetchData]);

  return {
    data,
    loading,
    error,
    refetch,
    setData, // Allow manual data updates
  };
}
