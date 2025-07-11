# backend/src/utils/audio_helpers.py
# This file is a placeholder for audio conversion utilities.
# For example, you might need to convert between WAV, MP3, and telephony-specific
# formats like G.711 (ulaw/alaw).

import subprocess

def convert_to_ulaw(input_wav_path: str, output_ulaw_path: str):
    """
    Converts a standard WAV file to a G.711 u-law formatted file
    using FFmpeg. This is a common format for VoIP.

    Requires ffmpeg to be installed on the system.
    """
    command = [
        'ffmpeg',
        '-i', input_wav_path,
        '-f', 'mulaw',          # Format is mu-law
        '-ar', '8000',           # Sample rate 8000 Hz
        '-ac', '1',              # Mono audio
        '-y',                    # Overwrite output file if it exists
        output_ulaw_path
    ]
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully converted {input_wav_path} to {output_ulaw_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting audio file: {e.stderr}")
        raise