export function ChartSkeleton() {
  return (
    <div
      className="relative h-[640px] w-full overflow-hidden"
      role="status"
      aria-label="Loading chart"
    >
      <svg
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
        className="absolute inset-0 h-full w-full animate-pulse motion-reduce:animate-none"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="skeletonArea" x1="0" y1="0" x2="0" y2="1">
            <stop
              offset="0%"
              stopColor="var(--color-faint)"
              stopOpacity="0.16"
            />
            <stop
              offset="100%"
              stopColor="var(--color-faint)"
              stopOpacity="0"
            />
          </linearGradient>
        </defs>
        <path
          d="M 0 78 L 8 74 L 16 80 L 24 70 L 34 72 L 44 60 L 54 64 L 64 50 L 74 54 L 84 42 L 92 38 L 100 32 L 100 100 L 0 100 Z"
          fill="url(#skeletonArea)"
        />
        <path
          d="M 0 78 L 8 74 L 16 80 L 24 70 L 34 72 L 44 60 L 54 64 L 64 50 L 74 54 L 84 42 L 92 38 L 100 32"
          fill="none"
          stroke="var(--color-faint)"
          strokeOpacity="0.4"
          strokeWidth="1"
          vectorEffect="non-scaling-stroke"
        />
      </svg>
    </div>
  );
}
