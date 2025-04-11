import os
import sys
from main import app
from utils import setup_logging, cleanup_old_files

# Setup logging
setup_logging()

# Clean up old files
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'call_logs')

cleanup_old_files(static_dir, max_age_days=2)  # Clean up audio files older than 2 days
cleanup_old_files(logs_dir, max_age_days=30)   # Clean up logs older than 30 days

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port)
