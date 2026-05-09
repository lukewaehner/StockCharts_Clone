export type IndicatorKey = "ma" | "bb" | "rsi" | "macd";

export type ChartMode = "simple" | "pro";

export type TimeRangeKey =
  | "month"
  | "3 months"
  | "6 months"
  | "year"
  | "2 years"
  | "5 years"
  | "10 years"
  | "ytd"
  | "max";

export interface Candle {
  time: number;
  open: number | null;
  high: number | null;
  low: number | null;
  close: number | null;
}

export interface VolumeBar {
  time: number;
  value: number;
  color: string;
}

export interface LinePoint {
  time: number;
  value: number;
}

export interface HistogramPoint {
  time: number;
  value: number;
  color: string;
}

export interface MaIndicator {
  short: { period: number; data: LinePoint[] };
  long: { period: number; data: LinePoint[] };
}

export interface BbIndicator {
  period: number;
  upper: LinePoint[];
  middle: LinePoint[];
  lower: LinePoint[];
}

export interface RsiIndicator {
  period: number;
  data: LinePoint[];
}

export interface MacdIndicator {
  line: LinePoint[];
  signal: LinePoint[];
  histogram: HistogramPoint[];
}

export interface StockSummary {
  price: number | null;
  change: number | null;
  changePct: number | null;
  open: number | null;
  prevClose: number | null;
  high: number | null;
  low: number | null;
  volume: number | null;
}

export interface KeyStats {
  marketCap: number | null;
  trailingPE: number | null;
  forwardPE: number | null;
  trailingEps: number | null;
  beta: number | null;
  dividendYield: number | null;
  fiftyTwoWeekHigh: number | null;
  fiftyTwoWeekLow: number | null;
  averageVolume: number | null;
  targetMeanPrice: number | null;
}

export interface StockResponse {
  symbol: string;
  name: string;
  info: {
    exchange?: string | null;
    currency?: string | null;
    quoteType?: string | null;
  };
  summary: StockSummary;
  keyStats: KeyStats;
  candles: Candle[];
  volume: VolumeBar[];
  indicators: {
    ma?: MaIndicator;
    bb?: BbIndicator;
    rsi?: RsiIndicator;
    macd?: MacdIndicator;
  };
}
