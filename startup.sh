#!/bin/bash

# Azure Web App startup script for D365FO MCP Server
echo "Starting D365FO FastMCP Server..."

# Set environment variables  
export HOST=${HOST:-"0.0.0.0"}
export PORT=${PORT:-8000}
export PYTHONPATH="/home/site/wwwroot/src:$PYTHONPATH"

# Force pip usage and ignore Poetry
export PIP_DISABLE_PIP_VERSION_CHECK=1
export POETRY_ACTIVE=0

# Ensure we're in the correct directory
cd /home/site/wwwroot

# Install dependencies using pip only
echo "Installing dependencies with pip..."
python -m pip install --upgrade pip setuptools wheel
python -m pip install --no-cache-dir -r requirements.txt

# Install the package in development mode
echo "Installing package in development mode..."
python -m pip install --no-cache-dir -e .

# Verify installation
echo "Verifying installation..."
python -c "import d365fo_client; print('✓ Package imported successfully')" || exit 1

# Start the server using the app.py entry point
echo "Starting server on ${HOST}:${PORT}"
exec python app.py