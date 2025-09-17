#!/bin/bash

# Development server start script
# This script starts the FastAPI server with reload enabled for development

echo "🚀 Starting Roblox Outfit Marketplace Backend Server..."
echo "📱 Server will be available at: http://localhost:8000"
echo "📚 API Documentation will be at: http://localhost:8000/docs"
echo "📖 Alternative docs at: http://localhost:8000/redoc"
echo ""

# Start the server with reload enabled
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000