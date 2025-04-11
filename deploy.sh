#!/bin/bash

# Deployment script for Locksmith AI Assistant
# This script deploys the application to a production server

# Exit on error
set -e

echo "Starting deployment of Locksmith AI Assistant..."

# Check if docker and docker-compose are installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit the .env file with your actual credentials before continuing."
    exit 1
fi

# Build and start the containers
echo "Building and starting Docker containers..."
docker-compose build
docker-compose up -d

# Check if containers are running
echo "Checking if containers are running..."
if [ "$(docker ps -q -f name=locksmith-ai-assistant)" ]; then
    echo "Locksmith AI Assistant is now running!"
    
    # Get the container IP
    CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' locksmith-ai-assistant)
    
    echo "Container IP: $CONTAINER_IP"
    echo "Application is accessible at: http://localhost:5000"
    echo ""
    echo "To configure Nginx with SSL, follow these steps:"
    echo "1. Update the domain name in nginx.conf"
    echo "2. Set up DNS to point your domain to this server"
    echo "3. Install Nginx on the host machine"
    echo "4. Copy nginx.conf to /etc/nginx/sites-available/"
    echo "5. Create a symbolic link to /etc/nginx/sites-enabled/"
    echo "6. Install certbot for SSL certificate"
    echo "7. Run: certbot --nginx -d yourdomain.com"
    echo ""
    echo "For more details, see the documentation."
else
    echo "Error: Container is not running. Check docker logs for details."
    docker-compose logs
    exit 1
fi
