export function Footer() {
  return (
    <footer className="mt-8 border-t border-border py-6">
      <div className="flex flex-wrap items-center gap-3 num text-[11px] tracking-wide text-faint">
        <span>Data</span>
        <a
          href="https://finance.yahoo.com"
          target="_blank"
          rel="noopener noreferrer"
          className="text-muted transition hover:text-text"
        >
          Yahoo Finance
        </a>
        <span className="text-border-strong">·</span>
        <span>Built with</span>
        <a
          href="https://www.tradingview.com/lightweight-charts/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-muted transition hover:text-text"
        >
          Lightweight Charts
        </a>
        <span className="text-border-strong">·</span>
        <span>For research only. Not investment advice.</span>
      </div>
    </footer>
  );
}
