from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
import json
import logging
import datetime
from dotenv import load_dotenv
from functools import wraps

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            static_folder='website/static',
            template_folder='website/templates')

# Configure app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'locksmith-ai-assistant-secret-key')
app.config['CALL_LOGS_DIR'] = 'call_logs'
app.config['ADMIN_USERNAME'] = os.getenv('ADMIN_USERNAME', 'admin')
app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD', 'password')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("website.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import routes after app initialization to avoid circular imports
from website.routes import main_routes, auth_routes, api_routes

# Register blueprints
app.register_blueprint(main_routes.main)
app.register_blueprint(auth_routes.auth)
app.register_blueprint(api_routes.api)

# Import the original AI assistant app
from main import answer_call, handle_response

# Create routes for Twilio webhooks
@app.route("/answer", methods=['POST'])
def twilio_answer_call():
    """Handle incoming calls from Twilio"""
    return answer_call()

@app.route("/handle-response", methods=['POST'])
def twilio_handle_response():
    """Process user's speech response"""
    return handle_response()

if __name__ == "__main__":
    # Create necessary directories if they don't exist
    os.makedirs('call_logs', exist_ok=True)
    os.makedirs('website/static/css', exist_ok=True)
    os.makedirs('website/static/js', exist_ok=True)
    os.makedirs('website/static/img', exist_ok=True)
    
    # Run Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
