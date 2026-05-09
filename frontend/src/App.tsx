import { useEffect, useState } from "react";

import { Chart } from "./components/Chart";
import { ChartSkeleton } from "./components/ChartSkeleton";
import { Controls } from "./components/Controls";
import { EmptyState } from "./components/EmptyState";
import { Footer } from "./components/Footer";
import { Header } from "./components/Header";
import { KeyStats } from "./components/KeyStats";
import { PageRails } from "./components/PageRails";
import { TickerHero } from "./components/TickerHero";
import { useStock } from "./hooks/useStock";
import type { ChartMode, IndicatorKey, TimeRangeKey } from "./types";

const DEFAULT_SYMBOL = "AAPL";
const DEFAULT_RANGE: TimeRangeKey = "ytd";
const DEFAULT_INDICATORS: IndicatorKey[] = ["ma", "rsi", "macd"];
const DEFAULT_MODE: ChartMode = "simple";

const VALID_RANGES: TimeRangeKey[] = [
  "month",
  "3 months",
  "6 months",
  "year",
  "2 years",
  "5 years",
  "10 years",
  "ytd",
  "max",
];
const VALID_INDICATORS: IndicatorKey[] = ["ma", "bb", "rsi", "macd"];
const TICKER_RE = /^\^?[A-Z][A-Z0-9.\-]{0,8}$/;

type Theme = "light" | "dark";

interface InitialState {
  symbol: string;
  range: TimeRangeKey;
  mode: ChartMode;
  indicators: IndicatorKey[];
}

const readInitialTheme = (): Theme => {
  if (typeof document === "undefined") return "light";
  const attr = document.documentElement.getAttribute("data-theme");
  return attr === "dark" ? "dark" : "light";
};

const readInitialState = (): InitialState => {
  if (typeof window === "undefined") {
    return {
      symbol: DEFAULT_SYMBOL,
      range: DEFAULT_RANGE,
      mode: DEFAULT_MODE,
      indicators: DEFAULT_INDICATORS,
    };
  }
  const params = new URLSearchParams(window.location.search);
  const s = params.get("s");
  const r = params.get("r");
  const m = params.get("m");
  const i = params.get("i");

  const validIndicators = i
    ? (i.split(",").filter((x) =>
        VALID_INDICATORS.includes(x as IndicatorKey),
      ) as IndicatorKey[])
    : null;

  return {
    symbol: s && TICKER_RE.test(s) ? s : DEFAULT_SYMBOL,
    range: r && VALID_RANGES.includes(r as TimeRangeKey)
      ? (r as TimeRangeKey)
      : DEFAULT_RANGE,
    mode: m === "simple" || m === "pro" ? m : DEFAULT_MODE,
    indicators:
      validIndicators && validIndicators.length > 0
        ? validIndicators
        : DEFAULT_INDICATORS,
  };
};

function App() {
  const initial = readInitialState();
  const [symbol, setSymbol] = useState(initial.symbol);
  const [range, setRange] = useState<TimeRangeKey>(initial.range);
  const [indicators, setIndicators] = useState<IndicatorKey[]>(
    initial.indicators,
  );
  const [mode, setMode] = useState<ChartMode>(initial.mode);
  const [theme, setTheme] = useState<Theme>(readInitialTheme);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    document.documentElement.style.colorScheme = theme;
    try {
      localStorage.setItem("theme", theme);
    } catch {
      // ignore quota / privacy-mode errors
    }
  }, [theme]);

  // Sync state to URL.
  useEffect(() => {
    const params = new URLSearchParams();
    if (symbol !== DEFAULT_SYMBOL) params.set("s", symbol);
    if (range !== DEFAULT_RANGE) params.set("r", range);
    if (mode !== DEFAULT_MODE) params.set("m", mode);
    if (mode === "pro" && indicators.length > 0) {
      params.set("i", indicators.join(","));
    }
    const search = params.toString();
    const next = search
      ? `${window.location.pathname}?${search}`
      : window.location.pathname;
    window.history.replaceState(null, "", next);
  }, [symbol, range, mode, indicators]);

  const activeIndicators = mode === "simple" ? [] : indicators;

  const { data, loading, error, fetchedAt, refetch } = useStock(
    symbol,
    range,
    activeIndicators,
  );

  const showSkeleton = loading && !data && !error;

  return (
    <>
      <PageRails data={data} fallbackSymbol={symbol} />
      <div className="relative mx-auto flex min-h-dvh max-w-[1400px] flex-col px-4 sm:px-8">
        <Header
          theme={theme}
          fetchedAt={fetchedAt}
          onThemeToggle={() =>
            setTheme((t) => (t === "light" ? "dark" : "light"))
          }
        />
        <TickerHero data={data} loading={loading} />
        <Controls
          symbol={symbol}
          range={range}
          indicators={indicators}
          mode={mode}
          onSymbolChange={setSymbol}
          onRangeChange={setRange}
          onIndicatorsChange={setIndicators}
          onModeChange={setMode}
        />
        <main className="flex-1 py-4">
          {error ? (
            <EmptyState
              variant="error"
              error={error}
              onRetry={refetch}
              onTrySuggestion={
                symbol !== "AAPL" ? () => setSymbol("AAPL") : undefined
              }
              suggestion="AAPL"
            />
          ) : showSkeleton ? (
            <ChartSkeleton />
          ) : data ? (
            <>
              <Chart
                data={data}
                indicators={activeIndicators}
                mode={mode}
                theme={theme}
              />
              <KeyStats data={data} />
            </>
          ) : (
            <EmptyState message="Enter a valid ticker to load chart data" />
          )}
        </main>
        <Footer />
      </div>
    </>
  );
}

export default App;
