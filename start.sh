#!/bin/bash

# Create necessary directories
mkdir -p static
mkdir -p call_logs

# Install required packages
pip install -r requirements.txt

# Start the application with gunicorn
gunicorn --bind 0.0.0.0:$PORT wsgi:app
