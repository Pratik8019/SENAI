#!/bin/bash
set -e

echo "🛡️  SentinelAI — Starting backend..."

# Run migrations
echo "📦 Running database migrations..."
alembic upgrade head

# Start server
echo "🚀 Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
