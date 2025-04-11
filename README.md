# Locksmith AI Assistant

A turn-key AI voice assistant that automatically answers incoming phone calls via Twilio and collects customer information for your locksmith business.

## Features

- **Natural Voice Interaction**: Uses ElevenLabs for natural-sounding female voice responses
- **Intelligent Conversation**: Powered by OpenAI GPT-3.5 for smart context awareness
- **Automated Information Collection**: Collects key customer information:
  - Customer's name
  - Phone number
  - Business name (if commercial)
  - Service requested
  - Vehicle details (if applicable)
  - Service location
- **Cloud Deployment**: Ready to deploy to Heroku or other cloud platforms
- **Twilio Integration**: Handles incoming calls through your Twilio phone number

## System Architecture

The Locksmith AI Assistant consists of several components:

1. **Twilio Voice Response**: Handles incoming calls and manages the conversation flow
2. **OpenAI GPT Integration**: Provides intelligent conversation capabilities
3. **ElevenLabs Voice Generation**: Creates natural-sounding voice responses
4. **Flask Web Application**: Serves as the backend for the entire system
5. **Cloud Deployment**: Hosted on Heroku for 24/7 availability

## Prerequisites

- Python 3.10 or higher
- Twilio account with a phone number
- OpenAI API key
- ElevenLabs API key
- Heroku account (for cloud deployment)
- Git (for deployment)

## Installation

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/locksmith-ai-assistant.git
   cd locksmith-ai-assistant
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create necessary directories:
   ```
   mkdir -p static call_logs
   ```

4. Run the application:
   ```
   python main.py
   ```

### Cloud Deployment

1. Make sure the deployment script is executable:
   ```
   chmod +x deploy_heroku.sh
   ```

2. Run the deployment script:
   ```
   ./deploy_heroku.sh
   ```

3. Configure Twilio to use your deployed application:
   ```
   chmod +x configure_twilio.sh
   ./configure_twilio.sh
   ```

## Configuration

The application uses environment variables for configuration. These can be set in a `.env` file for local development or configured on your cloud platform for deployment.

Required environment variables:

```
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

## Usage

### Conversation Flow

The AI assistant follows this conversation flow:

1. **Greeting**: "Thanks for calling the Locksmith, this is Angi, may I know your name?"
2. **Phone Number**: "What is the best number to call you back on?"
3. **Service Request**: "What service can we help you with?"
4. **Conditional Questions**:
   - If for a vehicle: "What is the make, model and year of the vehicle?"
   - If for a business: "What is the name of the business?"
   - If customer wants to go to a shop: "What city are you in?"
5. **Location**: "What is the address where you need help?"
6. **Closing**: "Ok, please stay by your phone, the technician will call you right back."

### Accessing Call Logs

Call logs are stored in the `call_logs` directory in JSON format. Each file contains the complete conversation data for a call, including:

- Customer name
- Phone number
- Business name (if applicable)
- Service requested
- Vehicle information (if applicable)
- Service location

## Maintenance

### Log Files

Log files are stored in the application directory:
- `app.log`: General application logs
- `error.log`: Error logs

### Cleaning Up Old Files

The application automatically cleans up:
- Audio files older than 2 days
- Log files older than 30 days

## Troubleshooting

### Common Issues

1. **Twilio webhook not working**:
   - Verify your application is running
   - Check that the Twilio phone number is configured with the correct webhook URL
   - Ensure your server is publicly accessible

2. **ElevenLabs voice generation failing**:
   - Check your ElevenLabs API key
   - Verify you have sufficient credits in your ElevenLabs account
   - The application will automatically fall back to Twilio's TTS if ElevenLabs fails

3. **OpenAI integration issues**:
   - Verify your OpenAI API key
   - Check for rate limiting or quota issues
   - The application includes fallback responses if the OpenAI API fails

## Support

For support, please contact your system administrator or the developer who set up this system.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
