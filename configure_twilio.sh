#!/bin/bash

# This script configures Twilio to use your deployed application as a webhook

# Check if Twilio CLI is installed
if ! command -v twilio &> /dev/null; then
    echo "Twilio CLI is not installed. Please install it first."
    echo "Visit: https://www.twilio.com/docs/twilio-cli/quickstart"
    exit 1
fi

# Check if logged in to Twilio
twilio profiles:list | grep active &> /dev/null
if [ $? -ne 0 ]; then
    echo "You are not logged in to Twilio. Please login first."
    twilio login
fi

# Get the deployed app URL
read -p "Enter your deployed app URL (e.g., https://locksmith-ai-assistant.herokuapp.com): " APP_URL

# Validate URL format
if [[ ! $APP_URL =~ ^https?:// ]]; then
    echo "Invalid URL format. URL must start with http:// or https://"
    exit 1
fi

# Configure Twilio phone number to use the webhook
echo "Configuring Twilio phone number +16282579348 to use webhook at $APP_URL/answer"
twilio phone-numbers:update +16282579348 --voice-url="$APP_URL/answer"

# Verify configuration
echo "Verifying configuration..."
twilio phone-numbers:fetch +16282579348

echo "Twilio webhook configuration complete!"
echo "Your Locksmith AI Assistant is now ready to receive calls at +16282579348"
echo "When someone calls this number, Twilio will forward the call to your application at $APP_URL/answer"
