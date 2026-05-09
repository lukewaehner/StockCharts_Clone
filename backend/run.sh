#!/usr/bin/env bash
# Run the FastAPI backend on http://127.0.0.1:8000
# Auto-creates .venv and installs requirements on first run.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "› creating backend venv"
  python3 -m venv .venv
  .venv/bin/pip install --upgrade pip >/dev/null
  .venv/bin/pip install -q -r requirements.txt
fi

exec .venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
