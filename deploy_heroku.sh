#!/bin/bash

# Production deployment script for Locksmith AI Assistant
# This script deploys the application to a production server using Heroku

# Exit on error
set -e

echo "Starting production deployment of Locksmith AI Assistant to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Heroku CLI is not installed. Installing now..."
    curl https://cli-assets.heroku.com/install.sh | sh
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install Git first."
    exit 1
fi

# Check if logged in to Heroku
heroku whoami &> /dev/null || {
    echo "Not logged in to Heroku. Please login:"
    heroku login
}

# Create Heroku app if it doesn't exist
APP_NAME="locksmith-ai-assistant"
if ! heroku apps:info --app $APP_NAME &> /dev/null; then
    echo "Creating Heroku app: $APP_NAME"
    heroku create $APP_NAME
else
    echo "Using existing Heroku app: $APP_NAME"
fi

# Initialize git if needed
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
fi

# Add Heroku remote if it doesn't exist
if ! git remote | grep heroku &> /dev/null; then
    echo "Adding Heroku remote..."
    heroku git:remote --app $APP_NAME
fi

# Set Heroku buildpack
echo "Setting Heroku buildpacks..."
heroku buildpacks:clear --app $APP_NAME
heroku buildpacks:set heroku/python --app $APP_NAME

# Configure environment variables
echo "Setting environment variables..."
heroku config:set \
    TWILIO_ACCOUNT_SID="AC27ce43e7ed60895230a5246b32a5b247" \
    TWILIO_AUTH_TOKEN="0dd96d4c661ccc6bdba1f11137cdaeed" \
    TWILIO_PHONE_NUMBER="+16282579348" \
    OPENAI_API_KEY="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" \
    ELEVENLABS_API_KEY="sk_708f56e2c500b056f005fae190dbe0a53f2014b697c2b2ca" \
    SECRET_KEY="$(openssl rand -hex 32)" \
    ADMIN_USERNAME="admin" \
    ADMIN_PASSWORD="locksmith2025" \
    --app $APP_NAME

# Deploy to Heroku
echo "Deploying to Heroku..."
git push heroku master

# Scale dynos
echo "Scaling dynos..."
heroku ps:scale web=1 --app $APP_NAME

# Configure Twilio webhook
echo "Configuring Twilio webhook..."
HEROKU_URL=$(heroku info --app $APP_NAME | grep "Web URL" | awk '{print $3}')
echo "Your Heroku URL is: $HEROKU_URL"
echo "Please update your Twilio phone number webhook to: ${HEROKU_URL}answer"

echo "Deployment completed successfully!"
echo "Your application is now available at: $HEROKU_URL"
echo ""
echo "Next steps:"
echo "1. Configure a custom domain (optional):"
echo "   heroku domains:add yourdomain.com --app $APP_NAME"
echo "2. Update your DNS settings to point to Heroku"
echo "3. Access the admin interface at: ${HEROKU_URL}login"
echo "   Username: admin"
echo "   Password: locksmith2025"
echo ""
echo "For more details, see the documentation."
