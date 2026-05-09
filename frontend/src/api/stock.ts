import type { IndicatorKey, StockResponse, TimeRangeKey } from "../types";

export async function fetchStock(
  symbol: string,
  range: TimeRangeKey,
  indicators: IndicatorKey[],
  signal?: AbortSignal,
): Promise<StockResponse> {
  const params = new URLSearchParams({
    range,
    indicators: indicators.join(","),
  });
  const res = await fetch(
    `/api/stock/${encodeURIComponent(symbol)}?${params.toString()}`,
    { signal },
  );
  if (!res.ok) {
    const detail = await res
      .json()
      .then((b) => b.detail as string)
      .catch(() => res.statusText);
    throw new Error(detail || `Request failed (${res.status})`);
  }
  return res.json();
}
