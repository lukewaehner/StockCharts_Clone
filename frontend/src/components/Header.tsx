interface HeaderProps {
  theme: "light" | "dark";
  fetchedAt: number | null;
  onThemeToggle: () => void;
}

const formatFetchedAt = (timestamp: number | null): string | null => {
  if (timestamp === null) return null;
  const formatter = new Intl.DateTimeFormat(undefined, {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
  return formatter.format(new Date(timestamp));
};

export function Header({ theme, fetchedAt, onThemeToggle }: HeaderProps) {
  const isDark = theme === "dark";
  const updated = formatFetchedAt(fetchedAt);
  return (
    <header className="flex items-center justify-between border-b border-border py-6">
      <div className="flex items-center gap-3">
        <div className="grid h-7 w-7 place-items-center rounded-md bg-accent text-on-dark text-[12px] font-semibold tracking-[-0.02em]">
          SC
        </div>
        <span className="text-[15px] font-semibold tracking-tight">
          StockCharts
        </span>
      </div>
      <div className="flex items-center gap-4">
        <span
          className="num hidden text-[11px] uppercase tracking-[0.06em] text-faint md:inline"
          aria-live="polite"
        >
          {updated ? `Updated ${updated} · Yahoo Finance` : "Yahoo Finance"}
        </span>
        <button
          type="button"
          onClick={onThemeToggle}
          aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
          title={isDark ? "Light mode" : "Dark mode"}
          className="grid h-8 w-8 place-items-center rounded-md border border-border bg-surface text-muted transition hover:text-text hover:border-border-strong focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/40"
        >
          {isDark ? (
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <circle cx="12" cy="12" r="4" />
              <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" />
            </svg>
          ) : (
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
            </svg>
          )}
        </button>
      </div>
    </header>
  );
}
