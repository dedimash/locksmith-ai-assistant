import os
import io
from google.cloud import speech
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GoogleSpeechToText:
    def __init__(self):
        """Initialize Google Speech-to-Text client"""
        self.client = speech.SpeechClient()
    
    def transcribe_audio(self, audio_content, language_code="en-US"):
        """
        Transcribe audio content using Google Cloud Speech-to-Text
        
        Args:
            audio_content (bytes): Audio content to transcribe
            language_code (str): Language code for transcription
            
        Returns:
            str: Transcribed text
        """
        # Configure audio settings
        audio = speech.RecognitionAudio(content=audio_content)
        
        # Configure recognition settings
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MULAW,
            sample_rate_hertz=8000,
            language_code=language_code,
            enable_automatic_punctuation=True,
            model="phone_call",  # Optimized for phone calls
            use_enhanced=True,   # Use enhanced model
        )
        
        # Perform speech recognition
        try:
            response = self.client.recognize(config=config, audio=audio)
            
            # Extract transcription results
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript
            
            return transcript
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return ""

# Function to convert Twilio audio format to format compatible with Google Speech API
def convert_twilio_audio(twilio_audio_url):
    """
    Download and convert Twilio audio to format compatible with Google Speech API
    
    Args:
        twilio_audio_url (str): URL to Twilio audio recording
        
    Returns:
        bytes: Audio content in appropriate format
    """
    import requests
    from pydub import AudioSegment
    
    # Download audio from Twilio
    response = requests.get(twilio_audio_url)
    
    if response.status_code == 200:
        # Save temporary WAV file
        temp_wav = "temp_audio.wav"
        with open(temp_wav, "wb") as f:
            f.write(response.content)
        
        # Convert to appropriate format for Google Speech API
        audio = AudioSegment.from_wav(temp_wav)
        
        # Export as bytes in memory
        buffer = io.BytesIO()
        audio.export(buffer, format="wav")
        
        # Clean up temporary file
        os.remove(temp_wav)
        
        return buffer.getvalue()
    else:
        print(f"Failed to download audio: {response.status_code}")
        return None
