#!/bin/bash
set -e

echo "Running database seed script..."
python scripts/seed_db.py

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
