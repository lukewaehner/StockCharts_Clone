#!/usr/bin/env bash
# Run the Vite dev server on http://localhost:5173
# Auto-installs node_modules on first run.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d node_modules ]; then
  echo "› installing frontend deps"
  npm install
fi

exec npm run dev
