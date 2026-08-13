#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT/frontend"
if [ -s "$HOME/.config/nvm/nvm.sh" ]; then
  # shellcheck disable=SC1091
  . "$HOME/.config/nvm/nvm.sh"
  nvm use 22 2>/dev/null || true
elif [ -s "$HOME/.nvm/nvm.sh" ]; then
  # shellcheck disable=SC1091
  . "$HOME/.nvm/nvm.sh"
  nvm use 22 2>/dev/null || true
fi
if [ ! -d node_modules ]; then
  npm install --legacy-peer-deps
fi
exec npm run dev
