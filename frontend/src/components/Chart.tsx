import { useEffect, useRef } from "react";
import {
  AreaSeries,
  CandlestickSeries,
  HistogramSeries,
  LineSeries,
  createChart,
  type IChartApi,
  type MouseEventParams,
  type UTCTimestamp,
} from "lightweight-charts";

import type {
  Candle,
  ChartMode,
  IndicatorKey,
  StockResponse,
} from "../types";

interface ChartProps {
  data: StockResponse | null;
  indicators: IndicatorKey[];
  mode: ChartMode;
  theme: "light" | "dark";
}

interface Theme {
  text: string;
  faint: string;
  border: string;
  grid: string;
  background: string;
  up: string;
  upSoft: string;
  down: string;
  downSoft: string;
  primary: string;
  secondary: string;
  tooltipBg: string;
}

const lightTheme: Theme = {
  text: "#0a0a0a",
  faint: "#a3a3a3",
  border: "#e5e5e5",
  grid: "#f0f0f0",
  background: "rgba(0,0,0,0)",
  up: "#047857",
  upSoft: "rgba(4, 120, 87, 0.18)",
  down: "#b91c1c",
  downSoft: "rgba(185, 28, 28, 0.18)",
  primary: "#0a0a0a",
  secondary: "#737373",
  tooltipBg: "rgba(255, 255, 255, 0.96)",
};

const darkTheme: Theme = {
  text: "#fafafa",
  faint: "#525252",
  border: "#262626",
  grid: "#1f1f1f",
  background: "rgba(0,0,0,0)",
  up: "#34d399",
  upSoft: "rgba(52, 211, 153, 0.22)",
  down: "#f87171",
  downSoft: "rgba(248, 113, 113, 0.22)",
  primary: "#fafafa",
  secondary: "#a3a3a3",
  tooltipBg: "rgba(20, 20, 20, 0.96)",
};

const cleanCandles = (raw: Candle[]) =>
  raw
    .filter(
      (c) =>
        c.open !== null &&
        c.high !== null &&
        c.low !== null &&
        c.close !== null,
    )
    .map((c) => ({
      time: c.time as UTCTimestamp,
      open: c.open as number,
      high: c.high as number,
      low: c.low as number,
      close: c.close as number,
    }));

const cleanLine = <T extends { time: number }>(arr: T[]) =>
  arr.map((p) => ({ ...p, time: p.time as UTCTimestamp }));

const closeSeries = (raw: Candle[]) =>
  raw
    .filter((c) => c.close !== null)
    .map((c) => ({
      time: c.time as UTCTimestamp,
      value: c.close as number,
    }));

const formatTooltipDate = (t: number) => {
  const d = new Date(t * 1000);
  return d.toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const formatTooltipPrice = (v: number) =>
  `$${v.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;

export function Chart({ data, indicators, mode, theme: themeName }: ChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    const tooltip = tooltipRef.current;
    if (!container || !data) return;

    const theme = themeName === "dark" ? darkTheme : lightTheme;
    const isSimple = mode === "simple";

    // Direction over the visible range — drives the green/red palette.
    const closes = data.candles.filter((c) => c.close !== null);
    const first = closes[0]?.close ?? null;
    const last = closes[closes.length - 1]?.close ?? null;
    const trendUp = first !== null && last !== null ? last >= first : true;
    const trendColor = trendUp ? theme.up : theme.down;
    const trendSoft = trendUp ? theme.upSoft : theme.downSoft;

    const showRsi =
      !isSimple && indicators.includes("rsi") && !!data.indicators.rsi;
    const showMacd =
      !isSimple && indicators.includes("macd") && !!data.indicators.macd;
    const showMa =
      !isSimple && indicators.includes("ma") && !!data.indicators.ma;
    const showBb =
      !isSimple && indicators.includes("bb") && !!data.indicators.bb;

    const pricePaneIndex = showRsi ? 1 : 0;
    const macdPaneIndex = showRsi ? 2 : 1;

    const chart = createChart(container, {
      autoSize: true,
      layout: {
        background: { color: theme.background },
        textColor: theme.faint,
        fontFamily:
          '"Geist", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        fontSize: 11,
        attributionLogo: false,
      },
      grid: {
        vertLines: { color: isSimple ? "rgba(0,0,0,0)" : theme.grid },
        horzLines: { color: isSimple ? "rgba(0,0,0,0)" : theme.grid },
      },
      rightPriceScale: {
        borderColor: theme.border,
        borderVisible: false,
        scaleMargins: isSimple
          ? { top: 0.18, bottom: 0.08 }
          : { top: 0.1, bottom: 0.1 },
      },
      timeScale: {
        borderColor: theme.border,
        borderVisible: false,
        timeVisible: false,
        secondsVisible: false,
        fixLeftEdge: isSimple,
        fixRightEdge: isSimple,
      },
      crosshair: {
        mode: 1,
        vertLine: {
          color: theme.faint,
          width: 1,
          style: isSimple ? 0 : 3,
          labelBackgroundColor: theme.text,
          labelVisible: !isSimple,
        },
        horzLine: {
          color: theme.faint,
          width: 1,
          style: isSimple ? 0 : 3,
          labelBackgroundColor: theme.text,
          labelVisible: !isSimple,
        },
      },
      handleScroll: !isSimple,
      handleScale: !isSimple,
    });

    chartRef.current = chart;

    // ============================================================
    // SIMPLE MODE — Coinbase-style line + gradient
    // ============================================================
    if (isSimple) {
      const areaSeries = chart.addSeries(AreaSeries, {
        lineColor: trendColor,
        topColor: trendSoft,
        bottomColor: "rgba(0,0,0,0)",
        lineWidth: 2,
        priceLineVisible: true,
        priceLineColor: trendColor,
        priceLineStyle: 2,
        priceLineWidth: 1,
        lastValueVisible: true,
        crosshairMarkerVisible: true,
        crosshairMarkerRadius: 4,
        crosshairMarkerBorderColor: theme.background,
        crosshairMarkerBackgroundColor: trendColor,
        priceFormat: { type: "price", precision: 2, minMove: 0.01 },
      });
      areaSeries.setData(closeSeries(data.candles));

      // Floating tooltip — only in simple mode.
      const handleCrosshair = (param: MouseEventParams) => {
        if (!tooltip) return;
        if (
          !param.point ||
          param.point.x < 0 ||
          param.point.y < 0 ||
          !param.time ||
          !param.seriesData.size
        ) {
          tooltip.style.opacity = "0";
          return;
        }
        const seriesData = param.seriesData.get(areaSeries) as
          | { value: number }
          | undefined;
        if (!seriesData) {
          tooltip.style.opacity = "0";
          return;
        }
        const time = param.time as UTCTimestamp;
        tooltip.innerHTML = `
          <div class="text-[10px] font-medium uppercase tracking-[0.08em] text-faint">${formatTooltipDate(time as number)}</div>
          <div class="num mt-[2px] text-[15px] font-medium tracking-tight" style="color:${trendColor}">${formatTooltipPrice(seriesData.value)}</div>
        `;
        const { width: cw } = container.getBoundingClientRect();
        const tw = tooltip.offsetWidth;
        const margin = 12;
        let left = param.point.x + margin;
        if (left + tw + margin > cw) left = param.point.x - tw - margin;
        tooltip.style.left = `${Math.max(margin, left)}px`;
        tooltip.style.top = `${Math.max(margin, param.point.y - 40)}px`;
        tooltip.style.opacity = "1";
      };
      chart.subscribeCrosshairMove(handleCrosshair);

      chart.timeScale().fitContent();

      return () => {
        chart.unsubscribeCrosshairMove(handleCrosshair);
        chart.remove();
        chartRef.current = null;
      };
    }

    // ============================================================
    // PRO MODE — candlesticks + indicators (existing behavior)
    // ============================================================

    if (showRsi && data.indicators.rsi) {
      const rsiSeries = chart.addSeries(
        LineSeries,
        {
          color: theme.secondary,
          lineWidth: 2,
          priceLineVisible: false,
          lastValueVisible: false,
          priceFormat: { type: "price", precision: 1, minMove: 0.1 },
        },
        0,
      );
      rsiSeries.setData(cleanLine(data.indicators.rsi.data));
      rsiSeries.createPriceLine({
        price: 70,
        color: theme.down,
        lineWidth: 1,
        lineStyle: 2,
        axisLabelVisible: true,
        title: "70",
      });
      rsiSeries.createPriceLine({
        price: 30,
        color: theme.up,
        lineWidth: 1,
        lineStyle: 2,
        axisLabelVisible: true,
        title: "30",
      });
      rsiSeries.createPriceLine({
        price: 50,
        color: theme.faint,
        lineWidth: 1,
        lineStyle: 1,
        axisLabelVisible: false,
      });
    }

    const candleSeries = chart.addSeries(
      CandlestickSeries,
      {
        upColor: theme.up,
        downColor: theme.down,
        borderVisible: false,
        wickUpColor: theme.up,
        wickDownColor: theme.down,
        priceFormat: { type: "price", precision: 2, minMove: 0.01 },
      },
      pricePaneIndex,
    );
    candleSeries.setData(cleanCandles(data.candles));

    if (showMa && data.indicators.ma) {
      const ma20 = chart.addSeries(
        LineSeries,
        {
          color: theme.primary,
          lineWidth: 2,
          priceLineVisible: false,
          lastValueVisible: false,
          title: `MA${data.indicators.ma.short.period}`,
        },
        pricePaneIndex,
      );
      ma20.setData(cleanLine(data.indicators.ma.short.data));

      const ma50 = chart.addSeries(
        LineSeries,
        {
          color: theme.secondary,
          lineWidth: 2,
          lineStyle: 2,
          priceLineVisible: false,
          lastValueVisible: false,
          title: `MA${data.indicators.ma.long.period}`,
        },
        pricePaneIndex,
      );
      ma50.setData(cleanLine(data.indicators.ma.long.data));
    }

    if (showBb && data.indicators.bb) {
      const bbStyle = {
        color: theme.faint,
        lineWidth: 1 as const,
        lineStyle: 2,
        priceLineVisible: false,
        lastValueVisible: false,
      };
      const upper = chart.addSeries(
        LineSeries,
        { ...bbStyle, title: "BB Upper" },
        pricePaneIndex,
      );
      upper.setData(cleanLine(data.indicators.bb.upper));
      const lower = chart.addSeries(
        LineSeries,
        { ...bbStyle, title: "BB Lower" },
        pricePaneIndex,
      );
      lower.setData(cleanLine(data.indicators.bb.lower));
    }

    const volumeSeries = chart.addSeries(
      HistogramSeries,
      {
        priceFormat: { type: "volume" },
        priceScaleId: "",
        lastValueVisible: false,
        priceLineVisible: false,
      },
      pricePaneIndex,
    );
    volumeSeries.setData(
      cleanLine(
        data.volume.map((v) => ({
          time: v.time,
          value: v.value,
          color: v.color,
        })),
      ),
    );
    volumeSeries
      .priceScale()
      .applyOptions({ scaleMargins: { top: 0.82, bottom: 0 } });

    if (showMacd && data.indicators.macd) {
      const macdHist = chart.addSeries(
        HistogramSeries,
        {
          priceLineVisible: false,
          lastValueVisible: false,
        },
        macdPaneIndex,
      );
      macdHist.setData(cleanLine(data.indicators.macd.histogram));

      const macdLine = chart.addSeries(
        LineSeries,
        {
          color: theme.primary,
          lineWidth: 2,
          priceLineVisible: false,
          lastValueVisible: false,
          title: "MACD",
        },
        macdPaneIndex,
      );
      macdLine.setData(cleanLine(data.indicators.macd.line));

      const macdSignal = chart.addSeries(
        LineSeries,
        {
          color: theme.secondary,
          lineWidth: 2,
          lineStyle: 2,
          priceLineVisible: false,
          lastValueVisible: false,
          title: "Signal",
        },
        macdPaneIndex,
      );
      macdSignal.setData(cleanLine(data.indicators.macd.signal));
    }

    const panes = chart.panes();
    if (panes.length >= 2) {
      const stretchFactors: number[] = [];
      if (showRsi) stretchFactors.push(1.2);
      stretchFactors.push(4);
      if (showMacd) stretchFactors.push(1.2);
      stretchFactors.forEach((factor, i) => {
        if (panes[i]) panes[i].setStretchFactor(factor);
      });
    }

    chart.timeScale().fitContent();

    return () => {
      chart.remove();
      chartRef.current = null;
    };
  }, [data, indicators, mode, themeName]);

  return (
    <div className="relative">
      <div
        ref={containerRef}
        className="h-[640px] w-full"
        data-testid="chart-container"
      />
      <div
        ref={tooltipRef}
        className="pointer-events-none absolute z-10 rounded-md border border-border bg-surface px-3 py-2 opacity-0 shadow-[0_8px_24px_rgba(0,0,0,0.08)] transition-opacity duration-100"
        style={{ transform: "translateZ(0)" }}
      />
    </div>
  );
}
