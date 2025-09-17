#!/bin/bash

# Production server start script
# This script starts the FastAPI server for production deployment

echo "🚀 Starting Roblox Outfit Marketplace Backend Server (Production Mode)..."
echo "📱 Server will be available at: http://0.0.0.0:8000"
echo ""

# Start the server without reload for production
uvicorn server.main:app --host 0.0.0.0 --port 8000