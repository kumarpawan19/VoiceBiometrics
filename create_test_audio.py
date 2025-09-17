# record_with_pyaudio.py
import pyaudio
import wave
import os
import time

def find_microphone_devices():
    """Find available microphone devices"""
    p = pyaudio.PyAudio()
    microphones = []
    
    for i in range(p.get_device_count()):
        try:
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                # Prefer actual microphones over generic devices
                name = device_info['name'].lower()
                if any(keyword in name for keyword in ['microphone', 'mic', 'capture']):
                    microphones.append((i, device_info))
        except:
            continue
    
    p.terminate()
    return microphones

def record_audio(filename, duration=5, sample_rate=44100, device_id=None):
    """Record audio using PyAudio with device selection and error handling"""
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    
    p = pyaudio.PyAudio()
    
    print(f"\n📢 Speak for {duration} seconds...")
    print("Starting in 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    
    try:
        # Try to open stream with specific device or default
        if device_id is not None:
            print(f"Using device ID: {device_id}")
            stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=sample_rate,
                           input=True,
                           input_device_index=device_id,
                           frames_per_buffer=CHUNK)
        else:
            stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=sample_rate,
                           input=True,
                           frames_per_buffer=CHUNK)
    except OSError as e:
        print(f"❌ Error opening audio stream: {e}")
        if device_id is None:
            print("Trying to find and use a specific microphone device...")
            microphones = find_microphone_devices()
            if microphones:
                device_id, device_info = microphones[0]
                print(f"Found microphone: {device_info['name']} (ID: {device_id})")
                try:
                    stream = p.open(format=FORMAT,
                                   channels=CHANNELS,
                                   rate=sample_rate,
                                   input=True,
                                   input_device_index=device_id,
                                   frames_per_buffer=CHUNK)
                except OSError as e2:
                    print(f"❌ Still failed with specific device: {e2}")
                    p.terminate()
                    return False
            else:
                print("❌ No microphone devices found!")
                p.terminate()
                return False
        else:
            p.terminate()
            return False
    
    print("🔴 RECORDING NOW!")
    frames = []
    
    try:
        for _ in range(0, int(sample_rate / CHUNK * duration)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        
        print("✅ Recording complete!")
        
    except Exception as e:
        print(f"❌ Error during recording: {e}")
        stream.stop_stream()
        stream.close()
        p.terminate()
        return False
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save the audio
    try:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"📁 Saved to: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

# Create test_audio directory
os.makedirs("test_audio", exist_ok=True)

# Find available microphones
print("🔍 Detecting microphones...")
microphones = find_microphone_devices()

if microphones:
    print("Available microphones:")
    for i, (device_id, device_info) in enumerate(microphones):
        print(f"  {i+1}. {device_info['name']} (ID: {device_id})")
    
    # Use the first microphone found
    selected_device_id, selected_device = microphones[0]
    print(f"\n✅ Using: {selected_device['name']}")
else:
    print("⚠️  No specific microphones found, will try default device")
    selected_device_id = None

# Record three samples
print("="*50)
print("VOICE RECORDING SESSION")
print("="*50)

print("\n[1/3] ENROLLMENT SAMPLE")
success = record_audio("test_audio/enrollment_sample.wav", device_id=selected_device_id)
if not success:
    print("❌ Failed to record enrollment sample. Exiting.")
    exit(1)

input("\nPress Enter to continue...")

print("\n[2/3] VERIFICATION SAMPLE")
success = record_audio("test_audio/verification_sample.wav", device_id=selected_device_id)
if not success:
    print("❌ Failed to record verification sample. Exiting.")
    exit(1)

input("\nPress Enter to continue...")

print("\n[3/3] IMPOSTOR SAMPLE (use different voice)")
success = record_audio("test_audio/impostor_sample.wav", device_id=selected_device_id)
if not success:
    print("❌ Failed to record impostor sample. Exiting.")
    exit(1)

print("\n✅ All recordings complete!")