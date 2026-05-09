import type { StockError } from "../hooks/useStock";

interface EmptyStateProps {
  variant?: "info" | "error";
  message?: string;
  error?: StockError | null;
  onRetry?: () => void;
  onTrySuggestion?: () => void;
  suggestion?: string;
}

export function EmptyState({
  variant = "info",
  message = "Enter a valid ticker to load chart data",
  error,
  onRetry,
  onTrySuggestion,
  suggestion = "AAPL",
}: EmptyStateProps) {
  if (variant === "error") {
    const title = error?.title ?? "Something went wrong";
    const detail =
      error?.detail ?? "An unexpected error occurred while loading this chart.";
    return (
      <div
        role="alert"
        aria-live="polite"
        className="grid h-[640px] w-full place-items-center"
      >
        <div className="flex max-w-md flex-col items-center gap-5 text-center">
          <div className="grid h-10 w-10 place-items-center rounded-full border border-border bg-surface-2 text-muted">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.75"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <circle cx="12" cy="12" r="10" />
              <path d="M12 8v4M12 16h.01" />
            </svg>
          </div>
          <div className="flex flex-col gap-2">
            <h2 className="text-[15px] font-semibold tracking-tight text-text">
              {title}
            </h2>
            <p className="text-[13px] leading-relaxed text-muted">{detail}</p>
          </div>
          <div className="mt-1 flex items-center gap-2">
            {onRetry && (
              <button
                type="button"
                onClick={onRetry}
                className="h-8 rounded-md border border-border bg-surface px-3 text-[12px] font-medium tracking-tight text-text transition hover:border-border-strong focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/40"
              >
                Retry
              </button>
            )}
            {onTrySuggestion && (
              <button
                type="button"
                onClick={onTrySuggestion}
                className="num h-8 rounded-md px-3 text-[12px] font-medium tracking-tight text-faint transition hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/40"
              >
                Try {suggestion}
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="grid h-[640px] w-full place-items-center">
      <p className="text-[13px] text-faint">{message}</p>
    </div>
  );
}
