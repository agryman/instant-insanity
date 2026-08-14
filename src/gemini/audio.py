import os
from pydub import AudioSegment
from pydub.scipy_effects import high_pass_filter, low_pass_filter


def enrich_headset_audio(voiceover_dir="media/voiceovers"):
    """Automatically applies EQ to raw headset MP3s to make them sound richer."""
    if not os.path.exists(voiceover_dir):
        return

    for filename in os.listdir(voiceover_dir):
        if filename.endswith(".mp3") and not filename.startswith("processed_"):
            file_path = os.path.join(voiceover_dir, filename)

            # Load the raw hoarse MP3 file
            sound = AudioSegment.from_mp3(file_path)

            # 1. Clear out muddy low-end room rumble below 80Hz
            sound = high_pass_filter(sound, 80)

            # 2. Boost the "Warmth" frequencies (200Hz) by duplicating a low-passed layer
            # This simulates a +3dB proximity effect bass boost
            bass_layer = low_pass_filter(sound, 250).apply_gain(3)
            sound = sound.overlay(bass_layer, gain_during_overlay=-3)

            # 3. Smooth out the gravelly, hoarse throat scratch (3.5kHz range)
            # We slightly attenuate everything above 3.5kHz to remove the harsh edge
            sound = sound.low_pass_filter(3800)

            # Overwrite the original file so Manim uses the rich version instantly
            sound.export(file_path, format="mp3", bitrate="192k")
            print(file_path)
