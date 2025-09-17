# test_impostor.py
import requests

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "test_user_001"

print("="*50)
print("🚫 TESTING IMPOSTOR DETECTION")
print("     (Different voice should be rejected)")
print("="*50)

try:
    with open('../test_audio/impostor_sample.wav', 'rb') as f:
        files = {'file': f}
        response = requests.post(f'{BASE_URL}/auth/verify/{USER_ID}', files=files)
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"📊 Results:")
        print(f"   Verified: {'✅ YES' if result['verified'] else '❌ NO'}")
        print(f"   Similarity Score: {result['voice_similarity']:.4f}")
        print(f"   Threshold: 0.85")
        
        if not result['verified']:
            print("\n✅ SUCCESS: Impostor correctly rejected!")
            print("Security test PASSED - System can distinguish voices")
        else:
            print("\n⚠️ SECURITY ISSUE: Impostor was incorrectly verified!")
            print("The system failed to distinguish between different voices")
    else:
        print(f"❌ API Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")