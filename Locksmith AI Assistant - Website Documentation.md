# Locksmith AI Assistant - Website Documentation

## Overview

The Locksmith AI Assistant is a comprehensive voice-based AI system that automatically answers incoming phone calls via Twilio and collects key customer information. This web interface provides a dashboard to manage call logs, configure system settings, and administer user accounts.

## System Architecture

The system consists of the following components:

1. **Voice AI Assistant**: Powered by Twilio, OpenAI GPT-3.5, and ElevenLabs
2. **Web Dashboard**: Flask-based web application with user authentication
3. **Database**: JSON-based storage for call logs and system data
4. **Deployment**: Docker containerization for easy deployment

## Installation and Deployment

### Prerequisites

- Domain name (optional but recommended)
- Server with Docker and Docker Compose installed
- Twilio account with a phone number
- OpenAI API key
- ElevenLabs API key

### Deployment Options

#### Option 1: Docker Deployment

1. Clone the repository to your server
2. Run the deployment script:
   ```
   ./deploy.sh
   ```
3. Configure your domain and SSL:
   ```
   ./configure_domain_ssl.sh
   ```

#### Option 2: Heroku Deployment

1. Clone the repository to your local machine
2. Run the Heroku deployment script:
   ```
   ./deploy_heroku.sh
   ```
3. Follow the instructions provided by the script to complete the setup

#### Option 3: Production Server Deployment

1. Clone the repository to your production server
2. Run the production deployment script:
   ```
   ./deploy_production.sh
   ```
3. Configure your domain and SSL:
   ```
   ./configure_domain_ssl.sh
   ```

## Accessing the Web Interface

After deployment, you can access the web interface at:

- Docker/Production: `https://yourdomain.com` (or `http://your-server-ip:5000` if no domain is configured)
- Heroku: `https://locksmith-ai-assistant.herokuapp.com`

### Default Login Credentials

- Username: `admin`
- Password: As specified during deployment (check deployment logs)

**Important**: Change the default password immediately after first login.

## Using the Web Interface

### Dashboard

The dashboard provides an overview of your call activity:

- Total calls received
- Recent calls (last 24 hours)
- Most common service requested
- Charts showing call distribution by service type and date
- Recent call log table

### Call Logs

The call logs page allows you to:

- View all call records
- Search and filter calls by various criteria
- Export call data to CSV
- View detailed information for each call
- Add notes to call records

### Settings

The settings page allows you to configure:

- Twilio integration settings
- OpenAI API settings
- ElevenLabs voice settings
- Conversation script customization
- System maintenance options

### User Management

The user management page (admin only) allows you to:

- Add new users
- Edit existing user information
- Delete users
- Assign user roles (admin or regular user)

### System Management

The system management page provides:

- System status monitoring
- API configuration
- System logs viewing
- Maintenance tools (backup, cleanup, restart)

## Twilio Integration

The system integrates with Twilio to handle incoming calls:

1. Customer calls your Twilio phone number
2. Twilio forwards the call to your web application
3. The AI assistant engages in conversation with the customer
4. Customer information is collected and stored
5. Call details appear in your web dashboard

### Updating Twilio Webhook

If you change your domain or server, update your Twilio webhook URL:

1. Log in to your Twilio account
2. Navigate to Phone Numbers > Manage > Active Numbers
3. Select your phone number
4. Update the webhook URL in the Voice & Fax section to:
   `https://yourdomain.com/answer`

## Maintenance

### Backing Up Data

To back up your call logs and system data:

1. Go to the System Management page
2. Click "Create Backup" in the System Maintenance section
3. Download the backup file to a secure location

### Cleaning Up Old Logs

To remove old call logs:

1. Go to the System Management page
2. Select a time period in the "Clean Old Logs" section
3. Click "Clean" to remove logs older than the specified period

### Monitoring System Status

To check the status of system components:

1. Go to the System Management page
2. View the System Status section
3. Click "Check Status" to refresh the status information

## Troubleshooting

### Common Issues

1. **Twilio calls not connecting**:
   - Check Twilio webhook URL configuration
   - Verify your server is accessible from the internet
   - Check Twilio account balance

2. **Voice generation not working**:
   - Verify ElevenLabs API key is correct
   - Check ElevenLabs credit balance
   - Check system logs for specific errors

3. **OpenAI integration issues**:
   - Verify OpenAI API key is correct
   - Check OpenAI API usage limits
   - Check system logs for specific errors

### Viewing Logs

To view system logs:

1. Go to the System Management page
2. Scroll to the System Logs section
3. Select the desired log level
4. Click "Refresh" to update the logs

## Security Considerations

- Change the default admin password immediately after deployment
- Use HTTPS with a valid SSL certificate
- Regularly update system components
- Back up your data regularly
- Use strong passwords for all accounts
- Limit admin access to trusted individuals

## Support and Contact

For support or questions about the Locksmith AI Assistant, please contact:

- Email: support@example.com
- Phone: (555) 123-4567

## License

This software is provided for the exclusive use of the Locksmith business and may not be redistributed without permission.
