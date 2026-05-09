import { useEffect, useRef, useState } from "react";

import type { ChartMode, IndicatorKey, TimeRangeKey } from "../types";

interface ControlsProps {
  symbol: string;
  range: TimeRangeKey;
  indicators: IndicatorKey[];
  mode: ChartMode;
  onSymbolChange: (symbol: string) => void;
  onRangeChange: (range: TimeRangeKey) => void;
  onIndicatorsChange: (indicators: IndicatorKey[]) => void;
  onModeChange: (mode: ChartMode) => void;
}

const TICKER_RE = /^\^?[A-Z][A-Z0-9.\-]{0,8}$/;

const RANGES: { label: string; value: TimeRangeKey }[] = [
  { label: "1M", value: "month" },
  { label: "3M", value: "3 months" },
  { label: "6M", value: "6 months" },
  { label: "YTD", value: "ytd" },
  { label: "1Y", value: "year" },
  { label: "5Y", value: "5 years" },
  { label: "All", value: "max" },
];

const INDICATORS: {
  label: string;
  value: IndicatorKey;
  description: string;
}[] = [
  {
    label: "MA",
    value: "ma",
    description: "Moving Averages. 20-day and 50-day simple averages of close.",
  },
  {
    label: "Bollinger",
    value: "bb",
    description:
      "Bollinger Bands. 2 standard deviations around the 20-day moving average.",
  },
  {
    label: "RSI",
    value: "rsi",
    description:
      "Relative Strength Index. Momentum oscillator from 0 to 100. Above 70 overbought, below 30 oversold.",
  },
  {
    label: "MACD",
    value: "macd",
    description:
      "Moving Average Convergence Divergence. Trend-following momentum indicator.",
  },
];

const MODES: { label: string; value: ChartMode; description: string }[] = [
  {
    label: "Simple",
    value: "simple",
    description: "Single area line. Range-direction colored. No indicators.",
  },
  {
    label: "Pro",
    value: "pro",
    description: "Candlesticks with volume and optional indicator panes.",
  },
];

const PILL_BASE =
  "h-7 min-w-[40px] rounded-sm border px-3 text-[12px] font-medium leading-none tracking-tight transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/40";
const PILL_ACTIVE =
  "border-border bg-surface text-text shadow-[0_1px_0_rgba(10,10,10,0.04)]";
const PILL_INACTIVE =
  "border-transparent bg-transparent text-faint hover:text-text";

interface SegmentedProps<T extends string> {
  ariaLabel: string;
  options: { label: string; value: T; description?: string }[];
  value: T;
  onChange: (next: T) => void;
  minWidth?: number;
}

function Segmented<T extends string>({
  ariaLabel,
  options,
  value,
  onChange,
  minWidth = 40,
}: SegmentedProps<T>) {
  const refs = useRef<(HTMLButtonElement | null)[]>([]);

  const handleKey = (e: React.KeyboardEvent, currentIndex: number) => {
    if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
    e.preventDefault();
    const dir = e.key === "ArrowRight" ? 1 : -1;
    const next = (currentIndex + dir + options.length) % options.length;
    onChange(options[next].value);
    refs.current[next]?.focus();
  };

  return (
    <div
      role="radiogroup"
      aria-label={ariaLabel}
      className="flex h-9 items-stretch gap-[2px] rounded-md border border-border bg-surface-2 p-[3px]"
    >
      {options.map((opt, idx) => {
        const active = opt.value === value;
        return (
          <button
            key={opt.value}
            ref={(el) => {
              refs.current[idx] = el;
            }}
            type="button"
            role="radio"
            aria-checked={active}
            tabIndex={active ? 0 : -1}
            title={opt.description}
            onClick={() => onChange(opt.value)}
            onKeyDown={(e) => handleKey(e, idx)}
            style={{ minWidth }}
            className={`${PILL_BASE} ${active ? PILL_ACTIVE : PILL_INACTIVE}`}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}

export function Controls({
  symbol,
  range,
  indicators,
  mode,
  onSymbolChange,
  onRangeChange,
  onIndicatorsChange,
  onModeChange,
}: ControlsProps) {
  const [draft, setDraft] = useState(symbol);
  const [touched, setTouched] = useState(false);

  useEffect(() => {
    setDraft(symbol);
    setTouched(false);
  }, [symbol]);

  const trimmed = draft.trim();
  const valid = trimmed.length === 0 || TICKER_RE.test(trimmed);
  const showError = touched && trimmed.length > 0 && !valid;

  const commit = () => {
    setTouched(true);
    if (!valid || trimmed.length === 0) {
      setDraft(symbol);
      setTouched(false);
      return;
    }
    if (trimmed !== symbol) onSymbolChange(trimmed);
  };

  const toggleIndicator = (key: IndicatorKey) => {
    const set = new Set(indicators);
    if (set.has(key)) set.delete(key);
    else set.add(key);
    onIndicatorsChange(Array.from(set));
  };

  return (
    <section className="flex flex-wrap items-start gap-6 border-b border-border py-6">
      <div className="flex min-w-[240px] flex-col gap-2">
        <label
          htmlFor="ticker-input"
          className="text-[10px] font-medium uppercase tracking-[0.08em] text-faint"
        >
          Symbol
        </label>
        <input
          id="ticker-input"
          type="text"
          value={draft}
          maxLength={10}
          spellCheck={false}
          autoCapitalize="characters"
          placeholder="AAPL"
          aria-invalid={showError}
          aria-describedby={showError ? "ticker-error" : "ticker-hint"}
          className={`num h-9 rounded-md border bg-surface px-3 text-[13px] font-medium uppercase tracking-tight outline-none transition focus:ring-2 focus:ring-accent/30 ${
            showError
              ? "border-down focus:border-down focus:ring-down/20"
              : "border-border focus:border-accent"
          }`}
          onChange={(e) => {
            setDraft(e.target.value.toUpperCase());
            if (touched) setTouched(false);
          }}
          onBlur={commit}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.currentTarget.blur();
            }
          }}
        />
        {showError ? (
          <span
            id="ticker-error"
            role="alert"
            className="num text-[11px] text-down"
          >
            Use letters, digits, dots or dashes. Up to 10 characters.
          </span>
        ) : (
          <span id="ticker-hint" className="num text-[11px] text-faint">
            AAPL · TSLA · NVDA · MSFT · GOOGL
          </span>
        )}
      </div>

      <div className="flex flex-col gap-2">
        <span className="text-[10px] font-medium uppercase tracking-[0.08em] text-faint">
          Period
        </span>
        <Segmented
          ariaLabel="Time period"
          options={RANGES}
          value={range}
          onChange={onRangeChange}
          minWidth={40}
        />
      </div>

      <div className="ml-auto flex flex-col gap-2">
        <span className="text-[10px] font-medium uppercase tracking-[0.08em] text-faint">
          View
        </span>
        <Segmented
          ariaLabel="Chart view"
          options={MODES}
          value={mode}
          onChange={onModeChange}
          minWidth={64}
        />
      </div>

      {mode === "pro" && (
        <div className="flex w-full flex-col gap-2">
          <span className="text-[10px] font-medium uppercase tracking-[0.08em] text-faint">
            Indicators
          </span>
          <div
            role="group"
            aria-label="Technical indicators"
            className="flex h-9 w-fit items-stretch gap-[2px] rounded-md border border-border bg-surface-2 p-[3px]"
          >
            {INDICATORS.map((ind) => {
              const active = indicators.includes(ind.value);
              return (
                <button
                  key={ind.value}
                  type="button"
                  aria-pressed={active}
                  title={ind.description}
                  onClick={() => toggleIndicator(ind.value)}
                  style={{ minWidth: 64 }}
                  className={`${PILL_BASE} ${active ? PILL_ACTIVE : PILL_INACTIVE}`}
                >
                  {ind.label}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </section>
  );
}
