import os
from elevenlabs import generate, set_api_key
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

# Set ElevenLabs API key
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

class ElevenLabsVoice:
    def __init__(self):
        """Initialize ElevenLabs Voice Generator"""
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice - professional female voice
        self.model_id = "eleven_monolingual_v1"
    
    def generate_audio(self, text, output_path=None):
        """
        Generate audio from text using ElevenLabs API
        
        Args:
            text (str): Text to convert to speech
            output_path (str, optional): Path to save audio file. If None, a temporary file is created.
            
        Returns:
            str: Path to the generated audio file
        """
        try:
            # Generate audio from text
            audio = generate(
                text=text,
                voice=self.voice_id,
                model=self.model_id
            )
            
            # Create output path if not provided
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                output_path = temp_file.name
                temp_file.close()
            
            # Save audio to file
            with open(output_path, "wb") as f:
                f.write(audio)
            
            return output_path
        
        except Exception as e:
            print(f"Error generating audio with ElevenLabs: {e}")
            return None
    
    def cleanup_temp_file(self, file_path):
        """
        Clean up temporary audio file
        
        Args:
            file_path (str): Path to file to delete
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up temporary file: {e}")
