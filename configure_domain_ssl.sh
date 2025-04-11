#!/bin/bash

# Script to configure domain and SSL certificate for Locksmith AI Assistant

# Exit on error
set -e

echo "Starting domain and SSL certificate configuration..."

# Check if running in the sandbox environment
if [ "$(hostname)" = "sandbox" ]; then
    echo "This script is intended to be run on a production server."
    echo "In this sandbox environment, we'll provide instructions for domain and SSL configuration."
    
    cat > /home/ubuntu/domain-ssl-instructions.txt << EOF
DOMAIN AND SSL CONFIGURATION INSTRUCTIONS
========================================

1. DOMAIN CONFIGURATION
----------------------

Option 1: Using a custom domain with Heroku:
- Purchase a domain from a domain registrar (e.g., Namecheap, GoDaddy)
- Add the domain to your Heroku app:
  $ heroku domains:add yourdomain.com --app locksmith-ai-assistant
- Configure DNS settings with your domain registrar:
  - Add a CNAME record pointing to your Heroku app's domain
  - Example: CNAME yourdomain.com -> locksmith-ai-assistant.herokuapp.com

Option 2: Using a custom domain with your own server:
- Purchase a domain from a domain registrar
- Configure DNS settings to point to your server's IP address
  - Add an A record pointing to your server's IP
  - Example: A yourdomain.com -> 123.456.789.10

2. SSL CERTIFICATE CONFIGURATION
------------------------------

Option 1: SSL with Heroku:
- Heroku automatically provides SSL for custom domains
- Enable SSL on your Heroku app:
  $ heroku certs:auto:enable --app locksmith-ai-assistant

Option 2: SSL with Let's Encrypt on your own server:
- Install Certbot:
  $ apt-get update
  $ apt-get install certbot python3-certbot-nginx
- Obtain and configure SSL certificate:
  $ certbot --nginx -d yourdomain.com
- Certbot will automatically configure Nginx and set up auto-renewal

3. UPDATING TWILIO WEBHOOK
------------------------

After configuring your domain and SSL:
- Update your Twilio phone number webhook URL to use your custom domain:
  https://yourdomain.com/answer
- Log in to your Twilio account
- Navigate to Phone Numbers > Manage > Active Numbers
- Select your phone number
- Update the webhook URL in the Voice & Fax section

4. TESTING YOUR CONFIGURATION
---------------------------

- Verify your domain is working: https://yourdomain.com
- Verify SSL is properly configured (look for the lock icon in browser)
- Test the Twilio integration by calling your phone number
- Log in to the admin dashboard at: https://yourdomain.com/login

EOF
    
    echo "Domain and SSL configuration instructions created at /home/ubuntu/domain-ssl-instructions.txt"
    
else
    # This is the actual production domain and SSL configuration code
    
    # Prompt for domain name
    read -p "Enter your domain name (e.g., example.com): " DOMAIN_NAME
    
    if [ -z "$DOMAIN_NAME" ]; then
        echo "Domain name is required. Exiting."
        exit 1
    fi
    
    # Check if Nginx is installed
    if ! command -v nginx &> /dev/null; then
        echo "Nginx is not installed. Installing Nginx..."
        apt-get update
        apt-get install -y nginx
    fi
    
    # Configure Nginx for the domain
    echo "Configuring Nginx for domain: $DOMAIN_NAME"
    
    # Create Nginx configuration file
    cat > /etc/nginx/sites-available/locksmith-ai-assistant << EOF
server {
    listen 80;
    server_name $DOMAIN_NAME;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /static/ {
        alias /app/website/static/;
        expires 30d;
    }
}
EOF
    
    # Enable the site
    ln -sf /etc/nginx/sites-available/locksmith-ai-assistant /etc/nginx/sites-enabled/
    
    # Test Nginx configuration
    nginx -t
    
    # Restart Nginx
    systemctl restart nginx
    
    echo "Nginx configured for domain: $DOMAIN_NAME"
    
    # Install Certbot for SSL
    echo "Installing Certbot for SSL certificate..."
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
    
    # Obtain and configure SSL certificate
    echo "Obtaining SSL certificate for domain: $DOMAIN_NAME"
    certbot --nginx -d $DOMAIN_NAME
    
    echo "SSL certificate configured successfully!"
    
    # Update Twilio webhook URL
    echo "Please update your Twilio webhook URL to: https://$DOMAIN_NAME/answer"
    echo "1. Log in to your Twilio account"
    echo "2. Navigate to Phone Numbers > Manage > Active Numbers"
    echo "3. Select your phone number"
    echo "4. Update the webhook URL in the Voice & Fax section"
    
    echo "Domain and SSL configuration completed successfully!"
    echo "Your application is now accessible at: https://$DOMAIN_NAME"
fi
