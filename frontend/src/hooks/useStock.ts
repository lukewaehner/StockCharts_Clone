import { useEffect, useState } from "react";

import { fetchStock } from "../api/stock";
import type { IndicatorKey, StockResponse, TimeRangeKey } from "../types";

interface UseStockResult {
  data: StockResponse | null;
  loading: boolean;
  error: StockError | null;
  fetchedAt: number | null;
  refetchToken: number;
  refetch: () => void;
}

export interface StockError {
  kind: "not_found" | "network" | "unknown";
  title: string;
  detail: string;
}

const sanitizeError = (raw: unknown, symbol: string): StockError => {
  const message = raw instanceof Error ? raw.message : String(raw ?? "");
  const lower = message.toLowerCase();
  if (
    lower.includes("404") ||
    lower.includes("not found") ||
    lower.includes("no data")
  ) {
    return {
      kind: "not_found",
      title: `We couldn't find data for "${symbol}"`,
      detail: "Double-check the symbol, or try a different ticker.",
    };
  }
  if (
    lower.includes("network") ||
    lower.includes("failed to fetch") ||
    lower.includes("typeerror")
  ) {
    return {
      kind: "network",
      title: "Lost connection to the data source",
      detail: "The request didn't make it through. Check your network and retry.",
    };
  }
  return {
    kind: "unknown",
    title: "Something went wrong",
    detail: message || "An unexpected error occurred while loading this chart.",
  };
};

export function useStock(
  symbol: string,
  range: TimeRangeKey,
  indicators: IndicatorKey[],
): UseStockResult {
  const [data, setData] = useState<StockResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<StockError | null>(null);
  const [fetchedAt, setFetchedAt] = useState<number | null>(null);
  const [refetchToken, setRefetchToken] = useState(0);

  const indicatorsKey = indicators.slice().sort().join(",");

  useEffect(() => {
    if (!symbol.trim()) {
      setData(null);
      setError(null);
      setFetchedAt(null);
      return;
    }

    const controller = new AbortController();
    setLoading(true);
    setError(null);

    fetchStock(symbol, range, indicators, controller.signal)
      .then((d) => {
        setData(d);
        setError(null);
        setFetchedAt(Date.now());
      })
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setError(sanitizeError(err, symbol));
        setData(null);
        setFetchedAt(null);
      })
      .finally(() => {
        setLoading(false);
      });

    return () => controller.abort();
  }, [symbol, range, indicatorsKey, refetchToken]);

  return {
    data,
    loading,
    error,
    fetchedAt,
    refetchToken,
    refetch: () => setRefetchToken((n) => n + 1),
  };
}
