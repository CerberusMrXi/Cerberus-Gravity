#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT/backend"
if [ ! -d .venv ]; then
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -U pip -q
  pip install -r requirements.txt -q
else
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
export PYTHONPATH=.
exec python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
