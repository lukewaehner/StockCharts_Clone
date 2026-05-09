import type { StockResponse } from "../types";

interface TickerHeroProps {
  data: StockResponse | null;
  loading: boolean;
}

const fmt = (value: number | null | undefined): string => {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return value.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
};

const fmtVolume = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return "—";
  if (value >= 1e9) return `${(value / 1e9).toFixed(2)}B`;
  if (value >= 1e6) return `${(value / 1e6).toFixed(2)}M`;
  if (value >= 1e3) return `${(value / 1e3).toFixed(1)}K`;
  return value.toFixed(0);
};

export function TickerHero({ data, loading }: TickerHeroProps) {
  const symbol = data?.symbol ?? "—";
  const name = data?.name ?? (loading ? "Loading…" : "—");
  const summary = data?.summary;
  const direction = (summary?.change ?? 0) >= 0 ? "up" : "down";
  const arrow = direction === "up" ? "▲" : "▼";

  return (
    <section className="grid grid-cols-1 gap-12 border-b border-border py-12 md:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)]">
      <div className="flex min-w-0 flex-col gap-3">
        <div className="flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.08em] text-faint">
          <span>Ticker</span>
          <span className="num rounded-sm border border-border bg-surface-2 px-2 py-[2px] font-semibold normal-case tracking-tight text-text">
            {symbol}
          </span>
        </div>

        <div className="truncate text-[22px] font-semibold leading-tight tracking-tight">
          {name}
        </div>

        <div className="mt-2 flex items-center gap-4">
          <span className="num text-[44px] font-medium leading-none tracking-[-0.04em]">
            {summary?.price !== null && summary?.price !== undefined
              ? `$${fmt(summary.price)}`
              : "—"}
          </span>
          {summary?.change !== null && summary?.change !== undefined && (
            <span
              className={`num inline-flex items-center gap-1 rounded-sm border px-2 py-1 text-[13px] font-medium ${
                direction === "up"
                  ? "border-up/20 bg-up-soft text-up"
                  : "border-down/20 bg-down-soft text-down"
              }`}
            >
              <span className="text-[11px]">{arrow}</span>
              <span>{fmt(Math.abs(summary.change))}</span>
              <span>
                {summary.changePct !== null && summary.changePct !== undefined
                  ? `${summary.changePct >= 0 ? "+" : ""}${summary.changePct.toFixed(2)}%`
                  : ""}
              </span>
            </span>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 content-end gap-x-8 gap-y-4 border-t border-border pt-4 md:border-l md:border-t-0 md:pl-8 md:pt-0">
        <Stat label="Open" value={fmt(summary?.open)} />
        <Stat label="Prev Close" value={fmt(summary?.prevClose)} />
        <Stat label="Day High" value={fmt(summary?.high)} />
        <Stat label="Day Low" value={fmt(summary?.low)} />
        <Stat label="Volume" value={fmtVolume(summary?.volume)} />
        <Stat label="Exchange" value={data?.info.exchange ?? "—"} mono={false} />
      </div>
    </section>
  );
}

function Stat({
  label,
  value,
  mono = true,
}: {
  label: string;
  value: string;
  mono?: boolean;
}) {
  return (
    <div className="flex flex-col gap-[2px]">
      <span className="text-[10px] font-medium uppercase tracking-[0.08em] text-faint">
        {label}
      </span>
      <span
        className={`text-[14px] font-medium tracking-tight ${
          mono ? "num" : ""
        }`}
      >
        {value}
      </span>
    </div>
  );
}
