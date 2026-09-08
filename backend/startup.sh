#!/bin/bash
# startup.sh — Production entrypoint for the backend.
# Reads PORT from environment (injected by Render/Railway/Fly.io etc.).
# Falls back to 8000 for local dev.

set -e

PORT=${PORT:-8000}

echo "Starting Lumen API on port $PORT..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --workers 1
