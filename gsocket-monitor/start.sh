#!/bin/bash

# GSocket Monitor Startup Script

APP_DIR="/workspace/gsocket-monitor"
APP_FILE="$APP_DIR/app.py"

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Determine which Python command to use
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
fi

# Check if the main application file exists
if [ ! -f "$APP_FILE" ]; then
    echo "Error: Main application file $APP_FILE does not exist"
    exit 1
fi

echo "Starting GSocket Monitor Application..."
echo "Configuration: $($PYTHON_CMD $APP_FILE config 2>/dev/null || echo 'Could not load config')"

# Run the application with the monitor command
$PYTHON_CMD $APP_FILE monitor