#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
echo "=== CERBERUS GRAVITY Installer ==="
echo "Root: $ROOT"

# Backend
echo "[1/3] Backend virtualenv + deps..."
cd "$ROOT/backend"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -U pip setuptools wheel -q
pip install -r requirements.txt -q
echo "Backend OK"

# Frontend (prefer nvm node 22 if available)
echo "[2/3] Frontend deps..."
cd "$ROOT/frontend"
if [ -s "$HOME/.config/nvm/nvm.sh" ]; then
  # shellcheck disable=SC1091
  . "$HOME/.config/nvm/nvm.sh"
  nvm use 22 2>/dev/null || nvm install 22
elif [ -s "$HOME/.nvm/nvm.sh" ]; then
  # shellcheck disable=SC1091
  . "$HOME/.nvm/nvm.sh"
  nvm use 22 2>/dev/null || nvm install 22
fi
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
echo "Frontend OK"

echo "[3/3] Done."
echo ""
echo "Start backend:  cd $ROOT/backend && source .venv/bin/activate && PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000"
echo "Start frontend: cd $ROOT/frontend && npm run dev"
echo "API docs:       http://127.0.0.1:8000/docs"
echo "UI:             http://127.0.0.1:3000"
