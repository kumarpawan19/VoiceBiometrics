# check_recordings.py
import os
import wave

def check_wav_file(filepath):
    """Check WAV file properties"""
    if os.path.exists(filepath):
        with wave.open(filepath, 'rb') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            channels = wav_file.getnchannels()
            
            print(f"✅ {filepath}")
            print(f"   Duration: {duration:.2f} seconds")
            print(f"   Sample Rate: {rate} Hz")
            print(f"   Channels: {channels}")
            print(f"   File Size: {os.path.getsize(filepath)/1024:.2f} KB")
            return True
    else:
        print(f"❌ {filepath} not found")
        return False

print("="*50)
print("📁 CHECKING AUDIO FILES")
print("="*50)

files = [
    "../test_audio/enrollment_sample.wav",
    "../test_audio/verification_sample.wav",
    "../test_audio/impostor_sample.wav"
]

for file in files:
    check_wav_file(file)
    print()