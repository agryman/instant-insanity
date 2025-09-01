import os
import tempfile
from typing import Optional, Dict, Any, cast
from pathlib import Path

from google.cloud import texttospeech
from manim_voiceover.services.base import SpeechService


class GCPTextToSpeechService(SpeechService):
    """
    Google Cloud Platform Text-to-Speech service for Manim voiceover.
    
    Uses the Google Cloud Text-to-Speech API with the en-US-Chirp3-HD-Aoede voice
    by default, but allows customization of voice parameters.
    """
    
    def __init__(
        self,
        voice_name: str = "en-US-Chirp3-HD-Aoede",
        language_code: str = "en-US",
        audio_encoding: Optional[texttospeech.AudioEncoding] = None,
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
        volume_gain_db: float = 0.0,
        sample_rate_hertz: Optional[int] = None,
        credentials_path: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the GCP Text-to-Speech service.
        
        Args:
            voice_name: The name of the voice to use (default: en-US-Chirp3-HD-Aoede)
            language_code: The language code for the voice (default: en-US)
            audio_encoding: The audio encoding format (default: MP3)
            speaking_rate: Speaking rate/speed (0.25 to 4.0, default: 1.0)
            pitch: Speaking pitch (-20.0 to 20.0, default: 0.0)
            volume_gain_db: Volume gain in dB (-96.0 to 16.0, default: 0.0)
            sample_rate_hertz: Sample rate in Hz (optional)
            credentials_path: Path to GCP service account JSON file (optional)
            **kwargs: Additional arguments passed to parent SpeechService
        """
        super().__init__(**kwargs)
        
        # Set up GCP credentials if provided
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        # Initialize the GCP Text-to-Speech client
        self.client = texttospeech.TextToSpeechClient()
        
        # Store voice configuration
        self.voice_config = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )

        # Set default audio encoding if not provided
        if audio_encoding is None:
            audio_encoding = cast(texttospeech.AudioEncoding, texttospeech.AudioEncoding.MP3)
        
        # Store audio configuration
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=audio_encoding,
            speaking_rate=speaking_rate,
            pitch=pitch,
            volume_gain_db=volume_gain_db
        )
        
        # Set sample rate if provided
        if sample_rate_hertz:
            self.audio_config.sample_rate_hertz = sample_rate_hertz
    
    def generate_from_text(
        self, 
        text: str, 
        cache_dir: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate speech audio from text using GCP Text-to-Speech.
        
        Args:
            text: The text to convert to speech
            cache_dir: Directory to cache audio files (optional)
            **kwargs: Additional arguments (unused)
            
        Returns:
            Dict containing the path to the generated audio file and metadata
        """
        # Create synthesis input
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Perform the text-to-speech request
        try:
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=self.voice_config,
                audio_config=self.audio_config
            )
        except Exception as e:
            raise RuntimeError(f"Failed to synthesize speech: {str(e)}")
        
        # Determine output directory
        if cache_dir:
            output_dir = Path(cache_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = Path(tempfile.gettempdir())
        
        # Create a unique filename based on text hash and voice settings
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        voice_hash = hashlib.md5(
            f"{self.voice_config.name}_{self.audio_config.speaking_rate}_{self.audio_config.pitch}".encode()
        ).hexdigest()[:8]
        
        # Determine file extension based on audio encoding
        if self.audio_config.audio_encoding == texttospeech.AudioEncoding.MP3:
            extension = "mp3"
        elif self.audio_config.audio_encoding == texttospeech.AudioEncoding.WAV:
            extension = "wav"
        elif self.audio_config.audio_encoding == texttospeech.AudioEncoding.OGG_OPUS:
            extension = "ogg"
        else:
            extension = "mp3"  # Default fallback
        
        output_path = output_dir / f"gcp_tts_{text_hash}_{voice_hash}.{extension}"
        
        # Write the audio content to file
        with open(output_path, "wb") as out_file:
            out_file.write(response.audio_content)
        
        # Calculate approximate duration (rough estimate)
        # Note: For more accurate duration, you might want to use an audio library
        # like librosa or pydub to get the actual duration
        estimated_duration = len(text.split()) * 0.6 / self.audio_config.speaking_rate
        
        return {
            "original_audio": str(output_path),
            "duration": estimated_duration,
            "text": text,
            "voice_name": self.voice_config.name,
            "language_code": self.voice_config.language_code
        }
    
    def __str__(self) -> str:
        return f"GCPTextToSpeechService(voice={self.voice_config.name})"
