#!/bin/bash

# Script to deploy the Locksmith AI Assistant to a production server using Docker

# Exit on error
set -e

echo "Starting deployment to production server..."

# Check if running in the sandbox environment
if [ "$(hostname)" = "sandbox" ]; then
    echo "This script is intended to be run on a production server."
    echo "In this sandbox environment, we'll simulate the deployment process."
    
    # Create a simulated deployment directory
    mkdir -p /home/ubuntu/production-deployment
    cp -r /home/ubuntu/locksmith-ai-assistant/* /home/ubuntu/production-deployment/
    
    echo "Files copied to simulated production environment at /home/ubuntu/production-deployment/"
    
    # Create a .env file from the example
    cp /home/ubuntu/production-deployment/.env.example /home/ubuntu/production-deployment/.env
    
    echo "Created .env file from template"
    
    # Simulate starting the application
    echo "Simulating application startup..."
    echo "Application would now be running at http://localhost:5000"
    
    # Create a deployment summary
    cat > /home/ubuntu/deployment-summary.txt << EOF
DEPLOYMENT SUMMARY
=================

Deployment Type: Docker (Simulated)
Deployment Time: $(date)
Deployment Location: /home/ubuntu/production-deployment

NEXT STEPS
==========

In a real production environment, you would:

1. Run the application with Docker:
   $ cd /path/to/locksmith-ai-assistant
   $ docker-compose up -d

2. Configure Nginx as a reverse proxy:
   - Copy nginx.conf to /etc/nginx/sites-available/
   - Create symbolic link to /etc/nginx/sites-enabled/
   - Restart Nginx

3. Set up SSL with Let's Encrypt:
   $ certbot --nginx -d yourdomain.com

4. Configure your domain DNS to point to your server

5. Update Twilio webhook URL to https://yourdomain.com/answer

For actual deployment, use either:
- deploy.sh for Docker deployment
- deploy_heroku.sh for Heroku deployment

EOF
    
    echo "Deployment simulation completed successfully!"
    echo "See deployment summary at /home/ubuntu/deployment-summary.txt"
    
else
    # This is the actual production deployment code
    
    # Check if docker and docker-compose are installed
    if ! command -v docker &> /dev/null; then
        echo "Docker is not installed. Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "Docker Compose is not installed. Installing Docker Compose..."
        curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        echo "Creating .env file from template..."
        cp .env.example .env
        
        # Generate a random secret key
        SECRET_KEY=$(openssl rand -hex 32)
        sed -i "s/your-secret-key-here/$SECRET_KEY/g" .env
        
        # Set a secure admin password
        ADMIN_PASSWORD=$(openssl rand -base64 12)
        sed -i "s/your-secure-password-here/$ADMIN_PASSWORD/g" .env
        
        echo "Generated secure credentials:"
        echo "Admin Username: admin"
        echo "Admin Password: $ADMIN_PASSWORD"
        echo "Please save these credentials in a secure location."
    fi
    
    # Build and start the containers
    echo "Building and starting Docker containers..."
    docker-compose build
    docker-compose up -d
    
    # Check if containers are running
    if [ "$(docker ps -q -f name=locksmith-ai-assistant)" ]; then
        echo "Locksmith AI Assistant is now running!"
        echo "Application is accessible at: http://localhost:5000"
        
        # Install Nginx if not already installed
        if ! command -v nginx &> /dev/null; then
            echo "Installing Nginx..."
            apt-get update
            apt-get install -y nginx
        fi
        
        # Configure Nginx
        echo "Configuring Nginx..."
        cp nginx.conf /etc/nginx/sites-available/locksmith-ai-assistant
        ln -sf /etc/nginx/sites-available/locksmith-ai-assistant /etc/nginx/sites-enabled/
        
        # Test Nginx configuration
        nginx -t
        
        # Restart Nginx
        systemctl restart nginx
        
        echo "Nginx configured successfully!"
        echo "To set up SSL with Let's Encrypt, run:"
        echo "certbot --nginx -d yourdomain.com"
    else
        echo "Error: Container is not running. Check docker logs for details."
        docker-compose logs
        exit 1
    fi
fi
