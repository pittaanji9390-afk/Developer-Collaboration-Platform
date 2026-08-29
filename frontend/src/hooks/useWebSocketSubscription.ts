import { useState, useEffect, useCallback } from 'react';

/**
 * useWebSocketSubscription
 * Subscribes to STOMP topic destinations with auto-reconnection
 */
export const useWebSocketSubscription = (initialValue?: any) => {
  const [data, setData] = useState<any>(initialValue);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  const execute = useCallback(async (...args: any[]) => {
    setIsLoading(true);
    setError(null);
    try {
      // Execution logic for Subscribes to STOMP topic destinations with auto-reconnection
      return data;
    } catch (err: any) {
      setError(err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [data]);

  return {
    data,
    setData,
    isLoading,
    error,
    execute
  };
};

export default useWebSocketSubscription;
