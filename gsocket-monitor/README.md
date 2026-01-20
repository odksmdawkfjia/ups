# GSocket Access Monitor and Maintenance Application

This Python application monitors and maintains access to gsocket endpoints, providing continuous monitoring, automatic recovery, and maintenance features.

## Features

- Continuous monitoring of gsocket access
- Automatic restoration of access when connection fails
- Scheduled maintenance tasks
- Logging of all activities
- Configurable settings
- Command-line interface

## Prerequisites

- Python 3.x
- pip package manager

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The application provides several command-line options:

```bash
# Start continuous monitoring (default behavior)
python3 app.py monitor

# Check gsocket access once
python3 app.py check

# Perform maintenance tasks
python3 app.py maintain

# View current configuration
python3 app.py config
```

## Configuration

The application uses a JSON configuration file located at:
`/workspace/gsocket-monitor/config/settings.json`

Default configuration:
```json
{
    "monitor_interval": 60,
    "gsocket_endpoint": "localhost:8080",
    "max_retries": 3,
    "timeout": 10,
    "maintenance_enabled": true
}
```

### Configuration Options

- `monitor_interval`: Time in seconds between checks (default: 60)
- `gsocket_endpoint`: The gsocket endpoint to monitor (host:port or full URL)
- `max_retries`: Maximum number of attempts to restore access (default: 3)
- `timeout`: Connection timeout in seconds (default: 10)
- `maintenance_enabled`: Whether maintenance tasks are enabled (default: true)

## Logs

Application logs are stored in:
`/workspace/gsocket-monitor/logs/access.log`

Log rotation is handled automatically during maintenance.

## Maintenance Tasks

The application performs the following maintenance tasks:
- Cleaning old log files (older than 7 days)
- Checking disk space usage
- Service health checks