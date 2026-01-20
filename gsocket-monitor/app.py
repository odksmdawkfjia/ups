#!/usr/bin/env python3
"""
GSocket Access Monitor and Maintenance Application

This application monitors and maintains gsocket connections/access
"""

import json
import time
import os
import sys
import requests
import logging
from datetime import datetime
from pathlib import Path


class GSocketMonitor:
    def __init__(self):
        self.config = {}
        self.log_file = '/workspace/gsocket-monitor/logs/access.log'
        self.load_config()
        self.setup_logging()

    def setup_logging(self):
        """Setup logging to file and console"""
        # Ensure log directory exists
        log_dir = os.path.dirname(self.log_file)
        os.makedirs(log_dir, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('GSocketMonitor')
        self.logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def load_config(self):
        """Load configuration from file or create default"""
        config_path = '/workspace/gsocket-monitor/config/settings.json'
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            # Create default config
            self.config = {
                'monitor_interval': 60,  # seconds
                'gsocket_endpoint': 'localhost:8080',
                'max_retries': 3,
                'timeout': 10,
                'maintenance_enabled': True
            }
            self.save_config()

    def save_config(self):
        """Save configuration to file"""
        config_path = '/workspace/gsocket-monitor/config/settings.json'
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def log_message(self, message, level='INFO'):
        """Log a message to both file and console"""
        getattr(self.logger, level.lower())(message)

    def check_gsocket_access(self):
        """Check if gsocket endpoint is accessible"""
        self.log_message(f"Checking gsocket access to {self.config['gsocket_endpoint']}")
        
        url = self.config['gsocket_endpoint']
        
        # Handle both URL and host:port formats
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"
        
        try:
            response = requests.get(url, timeout=self.config['timeout'])
            
            if response.status_code >= 400:
                self.log_message(f"GSocket access failed - HTTP Code: {response.status_code}", 'ERROR')
                return False
            else:
                self.log_message(f"GSocket access successful - HTTP Code: {response.status_code}")
                return True
                
        except requests.exceptions.RequestException as e:
            self.log_message(f"GSocket access failed: {str(e)}", 'ERROR')
            return False

    def perform_maintenance(self):
        """Perform maintenance tasks"""
        if not self.config['maintenance_enabled']:
            self.log_message("Maintenance is disabled in configuration")
            return

        self.log_message("Performing maintenance tasks...")

        # Clean old log entries (older than 7 days)
        self.clean_logs()

        # Check disk space
        self.check_disk_space()

        # Other maintenance tasks could go here
        self.restart_services_if_needed()

        self.log_message("Maintenance tasks completed")

    def clean_logs(self):
        """Clean old log files"""
        log_dir = os.path.dirname(self.log_file)
        
        # Get all log files in directory
        for filename in os.listdir(log_dir):
            if filename.endswith('.log'):
                filepath = os.path.join(log_dir, filename)
                # Delete logs older than 7 days (7 * 24 * 60 * 60 seconds)
                if time.time() - os.path.getmtime(filepath) > 7 * 24 * 60 * 60:
                    os.remove(filepath)
                    self.log_message(f"Deleted old log file: {filepath}")

    def check_disk_space(self):
        """Check disk space usage"""
        total, used, free = shutil.disk_usage("/") if hasattr(shutil, 'disk_usage') else self._get_disk_usage()
        percent_used = round((used / total) * 100, 2)
        
        self.log_message(f"Disk usage: {percent_used}% ({free} bytes free)")
        
        if percent_used > 90:
            self.log_message(f"High disk usage detected: {percent_used}%", 'WARNING')

    def _get_disk_usage(self):
        """Fallback method to get disk usage if shutil.disk_usage is not available"""
        statvfs = os.statvfs("/")
        total = statvfs.f_frsize * statvfs.f_blocks
        free = statvfs.f_frsize * statvfs.f_bavail
        used = total - free
        return total, used, free

    def restart_services_if_needed(self):
        """Placeholder for service restart logic"""
        self.log_message("Service health check completed")

    def run(self):
        """Main monitoring loop"""
        self.log_message("Starting GSocket Monitor Application")
        
        while True:
            access_ok = self.check_gsocket_access()
            
            if not access_ok:
                self.log_message("Attempting to restore gsocket access...", 'WARNING')
                self.restore_access()
            
            self.perform_maintenance()
            
            self.log_message(f"Sleeping for {self.config['monitor_interval']} seconds")
            time.sleep(self.config['monitor_interval'])

    def restore_access(self):
        """Attempt to restore access when connection fails"""
        retries = self.config['max_retries']
        
        for i in range(1, retries + 1):
            self.log_message(f"Attempt {i}/{retries} to restore access")
            
            # Try to restore access through various methods
            restored = self.attempt_restore()
            
            if restored:
                self.log_message("Access restored successfully")
                return True
            
            time.sleep(5)  # Wait before next attempt
        
        self.log_message(f"Failed to restore access after {retries} attempts", 'ERROR')
        return False

    def attempt_restore(self):
        """Placeholder for actual restoration logic"""
        self.log_message("Running restoration procedures")
        
        # In a real implementation, this would perform actual restoration steps
        # such as restarting services, checking firewall rules, etc.
        return True


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        action = 'monitor'
    else:
        action = sys.argv[1]

    monitor = GSocketMonitor()

    if action == 'monitor':
        monitor.run()
    elif action == 'check':
        result = monitor.check_gsocket_access()
        sys.exit(0 if result else 1)
    elif action == 'maintain':
        monitor.perform_maintenance()
    elif action == 'config':
        print(json.dumps(monitor.config, indent=2))
    else:
        print("Usage: python app.py [monitor|check|maintain|config]")
        print("  monitor  - Start continuous monitoring (default)")
        print("  check    - Check gsocket access once")
        print("  maintain - Perform maintenance tasks")
        print("  config   - Show current configuration")
        sys.exit(1)


if __name__ == "__main__":
    import shutil  # Import here to avoid issues if not available
    
    if len(sys.argv) > 1 and sys.argv[1] in ['monitor', 'check', 'maintain', 'config']:
        main()
    else:
        print("GSocket Access Monitor and Maintenance Application")
        print("Use 'python app.py --help' for usage information")
        if len(sys.argv) == 1:
            # Default to monitor mode if no arguments
            main()