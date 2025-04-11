#!/bin/bash

# Create necessary directories
mkdir -p call_logs logs website/static

# Display instructions
echo "=== Locksmith AI Assistant Setup ==="
echo "Directories created successfully."
echo "Starting Docker containers..."

# Start Docker containers
docker-compose up -d

# Check if containers are running
echo "Checking if containers are running..."
docker ps | grep locksmith-ai-assistant

echo ""
echo "=== Setup Complete ==="
echo "You can access the Locksmith AI Assistant at: http://localhost:5000"
echo ""
echo "To view logs, run: docker-compose logs -f"
echo "To stop the service, run: docker-compose down"
