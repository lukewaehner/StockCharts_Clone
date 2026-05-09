import type { StockResponse } from "../types";

interface PageRailsProps {
  data: StockResponse | null;
  fallbackSymbol: string;
}

const RAIL_TEXT_CLASS =
  "num whitespace-nowrap text-[10px] font-medium uppercase tracking-[0.32em] text-faint";
const HAIRLINE_CLASS = "h-24 w-px bg-border";

export function PageRails({ data, fallbackSymbol }: PageRailsProps) {
  const symbol = data?.symbol ?? fallbackSymbol;
  const exchange = data?.info?.exchange ?? "Yahoo Finance";

  return (
    <div
      aria-hidden
      className="pointer-events-none fixed inset-0 z-0 hidden min-[1700px]:block"
    >
      <div className="relative mx-auto h-full max-w-[1720px]">
        <div className="absolute inset-y-0 left-0 flex w-12 items-center justify-center">
          <div className="flex flex-col items-center gap-6">
            <span className={HAIRLINE_CLASS} />
            <span
              className={RAIL_TEXT_CLASS}
              style={{
                writingMode: "vertical-rl",
                transform: "rotate(180deg)",
              }}
            >
              StockCharts · {symbol}
            </span>
            <span className={HAIRLINE_CLASS} />
          </div>
        </div>

        <div className="absolute inset-y-0 right-0 flex w-12 items-center justify-center">
          <div className="flex flex-col items-center gap-6">
            <span className={HAIRLINE_CLASS} />
            <span
              className={RAIL_TEXT_CLASS}
              style={{ writingMode: "vertical-rl" }}
            >
              {exchange} · For research only
            </span>
            <span className={HAIRLINE_CLASS} />
          </div>
        </div>
      </div>
    </div>
  );
}
