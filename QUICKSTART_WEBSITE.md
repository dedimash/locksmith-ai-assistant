# Locksmith AI Assistant - Quick Start Guide

This quick start guide will help you get your Locksmith AI Assistant website up and running quickly.

## Prerequisites

- Domain name (optional but recommended)
- Server with Docker and Docker Compose installed
- Twilio account with a phone number
- OpenAI API key
- ElevenLabs API key

## Deployment Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/locksmith-ai-assistant.git
cd locksmith-ai-assistant
```

### Step 2: Choose Your Deployment Method

#### Option A: Docker Deployment

```bash
./deploy.sh
```

#### Option B: Heroku Deployment

```bash
./deploy_heroku.sh
```

#### Option C: Production Server Deployment

```bash
./deploy_production.sh
```

### Step 3: Configure Domain and SSL

```bash
./configure_domain_ssl.sh
```

Follow the prompts to set up your domain and SSL certificate.

### Step 4: Access Your Website

- Docker/Production: `https://yourdomain.com` (or `http://your-server-ip:5000`)
- Heroku: `https://locksmith-ai-assistant.herokuapp.com`

### Step 5: Log In

- Username: `admin`
- Password: As specified during deployment (check deployment logs)

**Important**: Change the default password immediately after first login.

## Testing Your Setup

1. Call your Twilio phone number
2. Verify that the AI assistant answers and follows the conversation script
3. Check that call logs appear in your dashboard

## Next Steps

- Customize your conversation script in the Settings page
- Add additional users in the User Management page
- Set up regular backups in the System Management page

For more detailed information, refer to the full [Website Documentation](WEBSITE_DOCUMENTATION.md).
