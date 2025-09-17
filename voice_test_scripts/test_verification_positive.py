# test_verification_positive.py
import requests

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "test_user_001"

print("="*50)
print("🔍 TESTING POSITIVE VERIFICATION")
print("     (Same person, different recording)")
print("="*50)

try:
    with open('../test_audio/verification_sample.wav', 'rb') as f:
        files = {'file': f}
        response = requests.post(f'{BASE_URL}/auth/verify/{USER_ID}', files=files)
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"📊 Results:")
        print(f"   Verified: {'✅ YES' if result['verified'] else '❌ NO'}")
        print(f"   Similarity Score: {result['voice_similarity']:.4f}")
        print(f"   Threshold: 0.85")
        print(f"   Status: {'PASSED' if result['voice_similarity'] > 0.85 else 'FAILED'}")
        
        if result['verified']:
            print("\n✅ SUCCESS: Your voice was correctly verified!")
        else:
            print("\n⚠️ WARNING: Your voice was not verified. Score too low.")
            print("This might happen if the recording quality differs.")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")