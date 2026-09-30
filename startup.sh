#!/bin/bash

# Azure App Service startup script for Streamlit TODO app
# This script configures and starts the Streamlit application on Azure App Service

echo "Starting Streamlit TODO application..."

# Set default port if not specified
if [ -z "$PORT" ]; then
    export PORT=8000
fi

echo "Using port: $PORT"

# Start Streamlit with production settings
python -m streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=true \
    --browser.gatherUsageStats=false