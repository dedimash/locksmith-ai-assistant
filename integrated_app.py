import os
import json
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_from_directory
from dotenv import load_dotenv
from functools import wraps
import datetime

# Import the original AI assistant modules
from gpt_conversation import GPTConversationManager
from text_to_speech import ElevenLabsVoice
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client

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

# Initialize Twilio client
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

# Initialize services
gpt_manager = GPTConversationManager()
voice_generator = ElevenLabsVoice()

# Store conversation state
conversation_data = {}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Routes for website
@app.route('/')
def index():
    """Home page"""
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check credentials against configured admin credentials
        if (username == app.config['ADMIN_USERNAME'] and 
            password == app.config['ADMIN_PASSWORD']):
            
            session['logged_in'] = True
            session['username'] = username
            flash('You are now logged in', 'success')
            
            # Redirect to next parameter if available, otherwise to dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page with call logs summary"""
    # Get call logs
    call_logs = get_call_logs()
    
    # Calculate statistics
    total_calls = len(call_logs)
    recent_calls = len([log for log in call_logs if is_recent(log.get('timestamp', ''))])
    
    # Group calls by service type
    service_types = {}
    for log in call_logs:
        service = log.get('service_requested', 'Unknown')
        if service in service_types:
            service_types[service] += 1
        else:
            service_types[service] = 1
    
    return render_template('dashboard.html', 
                          total_calls=total_calls,
                          recent_calls=recent_calls,
                          service_types=service_types,
                          recent_call_logs=get_recent_call_logs(5))

@app.route('/calls')
@login_required
def calls():
    """Page displaying all call logs"""
    call_logs = get_call_logs()
    
    # Extract unique service types for filter dropdown
    service_types = set()
    for log in call_logs:
        service = log.get('service_requested')
        if service:
            service_types.add(service)
    
    return render_template('calls.html', call_logs=call_logs, service_types=service_types)

@app.route('/call/<timestamp>')
@login_required
def call_detail(timestamp):
    """Page displaying details of a specific call"""
    call_log = get_call_log_by_timestamp(timestamp)
    if call_log:
        return render_template('call_detail.html', call=call_log)
    flash('Call log not found', 'danger')
    return redirect(url_for('calls'))

@app.route('/settings')
@login_required
def settings():
    """Settings page"""
    return render_template('settings.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('website/static', filename)

# API Routes
@app.route('/api/calls', methods=['GET'])
@login_required
def api_get_calls():
    """API endpoint to get all call logs"""
    call_logs = get_call_logs()
    return jsonify({"success": True, "data": call_logs})

@app.route('/api/calls/recent', methods=['GET'])
@login_required
def api_get_recent_calls():
    """API endpoint to get recent call logs"""
    limit = request.args.get('limit', 5, type=int)
    call_logs = get_call_logs()
    recent_logs = call_logs[:limit]
    return jsonify({"success": True, "data": recent_logs})

@app.route('/api/calls/<timestamp>', methods=['GET'])
@login_required
def api_get_call(timestamp):
    """API endpoint to get a specific call log"""
    call_log = get_call_log_by_timestamp(timestamp)
    if call_log:
        return jsonify({"success": True, "data": call_log})
    return jsonify({"success": False, "message": "Call log not found"}), 404

@app.route('/api/stats', methods=['GET'])
@login_required
def api_get_stats():
    """API endpoint to get call statistics"""
    call_logs = get_call_logs()
    
    # Calculate statistics
    total_calls = len(call_logs)
    
    # Count calls by service type
    service_types = {}
    for log in call_logs:
        service = log.get('service_requested', 'Unknown')
        if service in service_types:
            service_types[service] += 1
        else:
            service_types[service] = 1
    
    # Count calls by day (last 7 days)
    calls_by_day = {}
    today = datetime.datetime.now().date()
    for i in range(7):
        day = today - datetime.timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        calls_by_day[day_str] = 0
    
    for log in call_logs:
        try:
            timestamp = log.get('timestamp', '')
            if timestamp:
                dt = datetime.datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                day_str = dt.strftime("%Y-%m-%d")
                if day_str in calls_by_day:
                    calls_by_day[day_str] += 1
        except:
            pass
    
    return jsonify({
        "success": True, 
        "data": {
            "total_calls": total_calls,
            "service_types": service_types,
            "calls_by_day": calls_by_day
        }
    })

@app.route('/api/settings', methods=['POST'])
@login_required
def api_update_settings():
    """API endpoint to update system settings"""
    data = request.json
    
    # In a real application, this would update environment variables or database settings
    # For this demo, we'll just return success
    return jsonify({"success": True, "message": "Settings updated successfully"})

# Twilio webhook routes
@app.route("/answer", methods=['POST'])
def answer_call():
    """Handle incoming calls from Twilio"""
    try:
        # Get the caller's phone number
        caller_number = request.values.get('From', '')
        call_sid = request.values.get('CallSid', '')
        
        logger.info(f"Received call from {caller_number} with SID {call_sid}")
        
        # Initialize conversation state for this call
        conversation_data[call_sid] = {
            'name': None,
            'phone_number': caller_number,
            'business_name': None,
            'service_requested': None,
            'vehicle_info': None,
            'service_location': None,
            'current_step': 'greeting'
        }
        
        # Create TwiML response
        response = VoiceResponse()
        
        # Generate greeting message with ElevenLabs
        greeting_text = "Thanks for calling the Locksmith, this is Angi, may I know your name?"
        
        # Try to use ElevenLabs for voice generation
        try:
            audio_path = voice_generator.generate_audio(greeting_text)
            
            if audio_path and os.path.exists(audio_path):
                # Move audio file to static directory
                static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'website/static')
                static_filename = f"greeting_{call_sid}.mp3"
                static_audio_path = os.path.join(static_dir, static_filename)
                
                # Copy file to static directory
                import shutil
                shutil.copy(audio_path, static_audio_path)
                voice_generator.cleanup_temp_file(audio_path)
                
                # Get public URL for the audio file
                public_url = request.url_root.rstrip('/') + url_for('serve_static', filename=static_filename)
                response.play(public_url)
                logger.info(f"Using ElevenLabs audio at {public_url}")
            else:
                # Fallback to Twilio's TTS if ElevenLabs fails
                response.say(greeting_text, voice="alice")
                logger.warning("Falling back to Twilio TTS for greeting")
        except Exception as e:
            # Fallback to Twilio's TTS if ElevenLabs fails
            response.say(greeting_text, voice="alice")
            logger.error(f"Error using ElevenLabs: {str(e)}")
        
        # Add gather for speech input
        gather = Gather(input='speech', action='/handle-response', method='POST', speech_timeout=3)
        response.append(gather)
        
        # If no input is received, retry
        response.redirect('/answer')
        
        return str(response)
    except Exception as e:
        logger.error(f"Error in answer_call: {str(e)}")
        response = VoiceResponse()
        response.say("We're sorry, but we're experiencing technical difficulties. Please try again later.")
        return str(response)

@app.route("/handle-response", methods=['POST'])
def handle_response():
    """Process user's speech response"""
    try:
        # Get call SID and speech result
        call_sid = request.values.get('CallSid', '')
        speech_result = request.values.get('SpeechResult', '')
        
        logger.info(f"Received response for call {call_sid}: {speech_result}")
        
        # Get current conversation state
        call_data = conversation_data.get(call_sid, {})
        if not call_data:
            # If call data is missing, initialize with defaults
            call_data = {
                'name': None,
                'phone_number': request.values.get('From', ''),
                'business_name': None,
                'service_requested': None,
                'vehicle_info': None,
                'service_location': None,
                'current_step': 'greeting'
            }
            logger.warning(f"Missing call data for {call_sid}, initializing new session")
        
        current_step = call_data.get('current_step', 'greeting')
        
        # Use GPT to process the response and determine next step
        gpt_response = gpt_manager.get_response(call_data, current_step, speech_result)
        ai_message = gpt_response["message"]
        next_step = gpt_response["next_step"]
        
        logger.info(f"GPT response for step {current_step}: {ai_message}")
        logger.info(f"Next step: {next_step}")
        
        # Update conversation state based on current step
        if current_step == 'greeting':
            call_data['name'] = speech_result
        elif current_step == 'phone_number':
            call_data['phone_number'] = speech_result
        elif current_step == 'service':
            call_data['service_requested'] = speech_result
        elif current_step == 'vehicle_info':
            call_data['vehicle_info'] = speech_result
        elif current_step == 'business_name':
            call_data['business_name'] = speech_result
        elif current_step == 'city':
            call_data['service_location'] = f"City: {speech_result}"
        elif current_step == 'location':
            call_data['service_location'] = speech_result
        
        # Update next step
        call_data['current_step'] = next_step
        
        # Create TwiML response
        response = VoiceResponse()
        
        # Try to use ElevenLabs for voice generation
        try:
            audio_path = voice_generator.generate_audio(ai_message)
            
            if audio_path and os.path.exists(audio_path):
                # Move audio file to static directory
                static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'website/static')
                static_filename = f"response_{call_sid}_{current_step}.mp3"
                static_audio_path = os.path.join(static_dir, static_filename)
                
                # Copy file to static directory
                import shutil
                shutil.copy(audio_path, static_audio_path)
                voice_generator.cleanup_temp_file(audio_path)
                
                # Get public URL for the audio file
                public_url = request.url_root.rstrip('/') + url_for('serve_static', filename=static_filename)
                response.play(public_url)
                logger.info(f"Using ElevenLabs audio at {public_url}")
            else:
                # Fallback to Twilio's TTS if ElevenLabs fails
                response.say(ai_message, voice="alice")
                logger.warning("Falling back to Twilio TTS for response")
        except Exception as e:
            # Fallback to Twilio's TTS if ElevenLabs fails
            response.say(ai_message, voice="alice")
            logger.error(f"Error using ElevenLabs: {str(e)}")
        
        # If conversation is not complete, gather next response
        if next_step != 'completed':
            gather = Gather(input='speech', action='/handle-response', method='POST', speech_timeout=5)
            response.append(gather)
        else:
            # Save the completed conversation data
            save_conversation_data(call_data)
        
        # Update conversation state
        conversation_data[call_sid] = call_data
        
        # If no input received, retry the current question
        if not speech_result:
            response.redirect('/handle-response')
        
        return str(response)
    except Exception as e:
        logger.error(f"Error in handle_response: {str(e)}")
        response = VoiceResponse()
        response.say("We're sorry, but we're experiencing technical difficulties. Please try again later.")
        return str(response)

# Helper functions
def get_call_logs():
    """Get all call logs"""
    logs = []
    logs_dir = app.config['CALL_LOGS_DIR']
    
    if not os.path.exists(logs_dir):
        return logs
    
    for filename in os.listdir(logs_dir):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(logs_dir, filename), 'r') as f:
                    log_data = json.load(f)
                    # Add timestamp from filename
                    timestamp = filename.replace('call_', '').replace('.json', '')
                    log_data['timestamp'] = timestamp
                    logs.append(log_data)
            except E
(Content truncated due to size limit. Use line ranges to read in chunks)