# Quick Start Guide - Locksmith AI Assistant

This guide will help you quickly deploy and configure your Locksmith AI Assistant.

## Step 1: Deploy to Heroku

1. Make sure you have Git and Heroku CLI installed on your system
2. Navigate to the project directory:
   ```
   cd locksmith-ai-assistant
   ```
3. Run the deployment script:
   ```
   ./deploy_heroku.sh
   ```
4. Note the URL of your deployed application (e.g., https://locksmith-ai-assistant.herokuapp.com)

## Step 2: Configure Twilio

1. Make sure you have Twilio CLI installed on your system
2. Run the Twilio configuration script:
   ```
   ./configure_twilio.sh
   ```
3. When prompted, enter the URL of your deployed application

## Step 3: Test Your Assistant

1. Call your Twilio phone number: +16282579348
2. Follow the conversation flow with the AI assistant
3. Check the call logs in your Heroku application dashboard or by accessing the logs directory

## Step 4: Monitor and Maintain

1. Monitor your application logs in the Heroku dashboard
2. Check call logs regularly to ensure information is being collected correctly
3. Update your OpenAI and ElevenLabs API keys if they expire

## Troubleshooting

If you encounter any issues:

1. Check the application logs in Heroku
2. Verify your API keys are correctly set in the Heroku environment variables
3. Ensure your Twilio phone number is correctly configured with the webhook URL

For more detailed information, refer to the README.md file.
