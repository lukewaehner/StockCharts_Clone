#!/usr/bin/env bash
# Boot the full stack: FastAPI backend (:8000) + Vite frontend (:5173).
# Vite proxies /api/* to the backend, so open http://localhost:5173
set -euo pipefail
cd "$(dirname "$0")"

cleanup() {
  kill 0 2>/dev/null || true
}
trap cleanup EXIT INT TERM

./backend/run.sh &
backend_pid=$!

./frontend/run.sh &
frontend_pid=$!

echo "› backend  pid=$backend_pid  http://127.0.0.1:8000"
echo "› frontend pid=$frontend_pid  http://localhost:5173"
echo "› ctrl-c to stop both"

wait
