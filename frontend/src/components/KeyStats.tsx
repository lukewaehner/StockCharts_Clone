import type { StockResponse } from "../types";

interface KeyStatsProps {
  data: StockResponse;
}

const DASH = "—";

const fmtPrice = (v: number | null | undefined): string => {
  if (v === null || v === undefined || Number.isNaN(v)) return DASH;
  return `$${v.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
};

const fmtNumber = (v: number | null | undefined, digits = 2): string => {
  if (v === null || v === undefined || Number.isNaN(v)) return DASH;
  return v.toLocaleString(undefined, {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
};

const fmtCompact = (v: number | null | undefined): string => {
  if (v === null || v === undefined || Number.isNaN(v)) return DASH;
  const abs = Math.abs(v);
  if (abs >= 1e12) return `${(v / 1e12).toFixed(2)}T`;
  if (abs >= 1e9) return `${(v / 1e9).toFixed(2)}B`;
  if (abs >= 1e6) return `${(v / 1e6).toFixed(2)}M`;
  if (abs >= 1e3) return `${(v / 1e3).toFixed(1)}K`;
  return v.toFixed(0);
};

// yfinance >= 0.2.50 returns dividendYield as a percentage (e.g. 0.5 = 0.5%).
const fmtPercent = (v: number | null | undefined): string => {
  if (v === null || v === undefined || Number.isNaN(v)) return DASH;
  return `${v.toFixed(2)}%`;
};

export function KeyStats({ data }: KeyStatsProps) {
  const stats = data.keyStats;

  const items: { label: string; value: string }[] = [
    { label: "Market Cap", value: fmtCompact(stats?.marketCap) },
    { label: "P/E (TTM)", value: fmtNumber(stats?.trailingPE) },
    { label: "Forward P/E", value: fmtNumber(stats?.forwardPE) },
    { label: "EPS (TTM)", value: fmtPrice(stats?.trailingEps) },
    { label: "Beta", value: fmtNumber(stats?.beta) },
    { label: "Div Yield", value: fmtPercent(stats?.dividendYield) },
    { label: "52W High", value: fmtPrice(stats?.fiftyTwoWeekHigh) },
    { label: "52W Low", value: fmtPrice(stats?.fiftyTwoWeekLow) },
    { label: "Avg Volume", value: fmtCompact(stats?.averageVolume) },
    { label: "1Y Target", value: fmtPrice(stats?.targetMeanPrice) },
  ];

  return (
    <section
      aria-label="Key statistics"
      className="mt-6 border-t border-border pt-8"
    >
      <div className="mb-5 text-[10px] font-medium uppercase tracking-[0.08em] text-faint">
        Key Stats
      </div>
      <div className="grid grid-cols-2 gap-x-8 gap-y-5 sm:grid-cols-3 md:grid-cols-5">
        {items.map((item) => (
          <Stat key={item.label} label={item.label} value={item.value} />
        ))}
      </div>
    </section>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col gap-[2px]">
      <span className="text-[10px] font-medium uppercase tracking-[0.08em] text-faint">
        {label}
      </span>
      <span className="num text-[14px] font-medium tracking-tight">
        {value}
      </span>
    </div>
  );
}
