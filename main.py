import os
from flask import Flask, request, url_for, send_from_directory
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from dotenv import load_dotenv
import json
import tempfile
import time

# Import custom modules
# Modified to use API key instead of service account
from gpt_conversation import GPTConversationManager
from text_to_speech import ElevenLabsVoice

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

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

@app.route("/", methods=['GET'])
def index():
    """Home page"""
    return "Twilio AI Assistant is running!"

@app.route("/static/<path:filename>")
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route("/answer", methods=['POST'])
def answer_call():
    """Handle incoming calls from Twilio"""
    # Get the caller's phone number
    caller_number = request.values.get('From', '')
    call_sid = request.values.get('CallSid', '')
    
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
    audio_path = voice_generator.generate_audio(greeting_text)
    
    # Move audio file to static directory
    if audio_path and os.path.exists(audio_path):
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        static_filename = f"greeting_{call_sid}.mp3"
        static_audio_path = os.path.join(static_dir, static_filename)
        
        # Move file to static directory
        import shutil
        shutil.copy(audio_path, static_audio_path)
        voice_generator.cleanup_temp_file(audio_path)
        
        # Get public URL for the audio file
        public_url = request.url_root.rstrip('/') + url_for('serve_static', filename=static_filename)
        response.play(public_url)
    else:
        # Fallback to Twilio's TTS if ElevenLabs fails
        response.say(greeting_text, voice="alice")
    
    # Add gather for speech input
    gather = Gather(input='speech', action='/handle-response', method='POST', speech_timeout=3)
    response.append(gather)
    
    # If no input is received, retry
    response.redirect('/answer')
    
    return str(response)

@app.route("/handle-response", methods=['POST'])
def handle_response():
    """Process user's speech response"""
    # Get call SID and speech result from Twilio
    call_sid = request.values.get('CallSid', '')
    speech_result = request.values.get('SpeechResult', '')
    
    # Get current conversation state
    call_data = conversation_data.get(call_sid, {})
    current_step = call_data.get('current_step', 'greeting')
    
    # Use GPT to process the response and determine next step
    gpt_response = gpt_manager.get_response(call_data, current_step, speech_result)
    ai_message = gpt_response["message"]
    next_step = gpt_response["next_step"]
    
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
    elif current_step == 'location':
        call_data['service_location'] = speech_result
    
    # Update next step
    call_data['current_step'] = next_step
    
    # Create TwiML response
    response = VoiceResponse()
    
    # Generate response with ElevenLabs
    audio_path = voice_generator.generate_audio(ai_message)
    
    # Move audio file to static directory
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    static_filename = f"response_{call_sid}_{current_step}.mp3"
    static_audio_path = os.path.join(static_dir, static_filename)
    
    if audio_path and os.path.exists(audio_path):
        # Move file to static directory
        import shutil
        shutil.copy(audio_path, static_audio_path)
        voice_generator.cleanup_temp_file(audio_path)
        
        # Get public URL for the audio file
        public_url = request.url_root.rstrip('/') + url_for('serve_static', filename=static_filename)
        response.play(public_url)
    else:
        # Fallback to Twilio's TTS if ElevenLabs fails
        response.say(ai_message, voice="alice")
    
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

def save_conversation_data(data):
    """Save the conversation data to a file"""
    # Create a directory for call logs if it doesn't exist
    os.makedirs('call_logs', exist_ok=True)
    
    # Generate a filename based on timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"call_logs/call_{timestamp}.json"
    
    # Write the data to a JSON file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Create static directory for audio files
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    os.makedirs(static_dir, exist_ok=True)
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
