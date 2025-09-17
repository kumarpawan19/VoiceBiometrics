# test_enrollment.py
import requests
import json

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "test_user_001"

print("="*50)
print("🎯 TESTING VOICE ENROLLMENT")
print("="*50)

# Enroll your voice
try:
    with open('../test_audio/enrollment_sample.wav', 'rb') as f:
        files = {'file': f}
        response = requests.post(f'{BASE_URL}/auth/enroll/{USER_ID}', files=files)
    
    if response.status_code == 200:
        print(f"✅ SUCCESS: {response.json()['message']}")
        print(f"User ID: {USER_ID}")
        print("Voice embedding stored in database!")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except FileNotFoundError:
    print("❌ File not found. Make sure enrollment_sample.wav exists in test_audio folder")
except Exception as e:
    print(f"❌ Error: {e}")