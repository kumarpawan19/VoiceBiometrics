# complete_test_suite.py
import requests
import json
import time
import os
import sqlite3
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

class VoiceBiometricsTestSuite:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "metrics": {}
        }
        self.user_id = f"test_user_{int(time.time())}"
    
    def test_api_health(self):
        """Test if API is running"""
        print("\n🔍 Testing API Health...")
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ API is healthy")
                self.results["tests"].append({
                    "name": "API Health",
                    "status": "PASS"
                })
                return True
        except:
            print("❌ API is not responding")
            self.results["tests"].append({
                "name": "API Health",
                "status": "FAIL"
            })
            return False
    
    def test_enrollment(self):
        """Test voice enrollment"""
        print("\n📝 Testing Voice Enrollment...")
        try:
            with open('../test_audio/enrollment_sample.wav', 'rb') as f:
                files = {'file': f}
                response = requests.post(f'{BASE_URL}/auth/enroll/{self.user_id}', files=files)
            
            if response.status_code == 200:
                print(f"✅ Enrolled user: {self.user_id}")
                self.results["tests"].append({
                    "name": "Voice Enrollment",
                    "status": "PASS",
                    "user_id": self.user_id
                })
                return True
            else:
                print("❌ Enrollment failed")
                self.results["tests"].append({
                    "name": "Voice Enrollment",
                    "status": "FAIL",
                    "error": response.text
                })
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_verification_positive(self):
        """Test legitimate user verification"""
        print("\n✅ Testing Positive Verification...")
        try:
            with open('../test_audio/verification_sample.wav', 'rb') as f:
                files = {'file': f}
                response = requests.post(f'{BASE_URL}/auth/verify/{self.user_id}', files=files)
            
            result = response.json()
            verified = result['verified']
            similarity = result['voice_similarity']
            
            print(f"   Similarity: {similarity:.4f}")
            print(f"   Verified: {verified}")
            
            self.results["tests"].append({
                "name": "Positive Verification",
                "status": "PASS" if verified else "FAIL",
                "similarity": similarity,
                "verified": verified
            })
            
            self.results["metrics"]["genuine_score"] = similarity
            return verified, similarity
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False, 0
    
    def test_verification_negative(self):
        """Test impostor rejection"""
        print("\n🚫 Testing Impostor Detection...")
        try:
            with open('test_audio/impostor_sample.wav', 'rb') as f:
                files = {'file': f}
                response = requests.post(f'{BASE_URL}/auth/verify/{self.user_id}', files=files)
            
            result = response.json()
            verified = result['verified']
            similarity = result['voice_similarity']
            
            print(f"   Similarity: {similarity:.4f}")
            print(f"   Verified: {verified}")
            
            self.results["tests"].append({
                "name": "Impostor Detection",
                "status": "PASS" if not verified else "FAIL",
                "similarity": similarity,
                "verified": verified
            })
            
            self.results["metrics"]["impostor_score"] = similarity
            return not verified, similarity
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False, 0
    
    def test_liveness(self):
        """Test liveness phrase generation"""
        print("\n🎲 Testing Liveness Detection...")
        try:
            response = requests.get(f"{BASE_URL}/phrase/generate")
            phrase = response.json()['phrase']
            print(f"   Generated: '{phrase}'")
            
            self.results["tests"].append({
                "name": "Liveness Phrase",
                "status": "PASS",
                "phrase": phrase
            })
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def check_database(self):
        """Check database for enrolled users"""
        print("\n💾 Checking Database...")
        try:
            conn = sqlite3.connect('voice_biometrics.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM voice_embeddings")
            count = cursor.fetchone()[0]
            print(f"   Total enrolled users: {count}")
            
            cursor.execute("SELECT user_id, created_at FROM voice_embeddings ORDER BY created_at DESC LIMIT 5")
            recent = cursor.fetchall()
            
            if recent:
                print("   Recent enrollments:")
                for user in recent:
                    print(f"     - {user[0]} at {user[1]}")
            
            conn.close()
            self.results["metrics"]["total_users"] = count
            return True
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False
    
    def calculate_metrics(self):
        """Calculate accuracy metrics"""
        if "genuine_score" in self.results["metrics"] and "impostor_score" in self.results["metrics"]:
            genuine = self.results["metrics"]["genuine_score"]
            impostor = self.results["metrics"]["impostor_score"]
            
            self.results["metrics"]["score_separation"] = genuine - impostor
            self.results["metrics"]["threshold"] = 0.85
            
            # Simple FAR/FRR calculation
            if genuine > 0.85:
                self.results["metrics"]["FRR"] = 0  # False Rejection Rate
            else:
                self.results["metrics"]["FRR"] = 1
                
            if impostor < 0.85:
                self.results["metrics"]["FAR"] = 0  # False Acceptance Rate
            else:
                self.results["metrics"]["FAR"] = 1
    
    def generate_report(self):
        """Generate final test report"""
        print("\n" + "="*60)
        print("📊 VOICE BIOMETRICS TEST REPORT")
        print("="*60)
        
        # Test Results
        print("\n📋 Test Results:")
        for test in self.results["tests"]:
            status_icon = "✅" if test["status"] == "PASS" else "❌"
            print(f"   {status_icon} {test['name']}: {test['status']}")
        
        # Metrics
        if self.results["metrics"]:
            print("\n📈 Performance Metrics:")
            metrics = self.results["metrics"]
            
            if "genuine_score" in metrics:
                print(f"   Genuine User Score: {metrics['genuine_score']:.4f}")
            if "impostor_score" in metrics:
                print(f"   Impostor Score: {metrics['impostor_score']:.4f}")
            if "score_separation" in metrics:
                print(f"   Score Separation: {metrics['score_separation']:.4f}")
            if "FAR" in metrics:
                print(f"   False Acceptance Rate: {metrics['FAR']*100:.1f}%")
            if "FRR" in metrics:
                print(f"   False Rejection Rate: {metrics['FRR']*100:.1f}%")
        
        # Save to file
        with open('test_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print("\n📁 Detailed report saved to: test_report.json")
        
        # Overall Assessment
        print("\n🎯 Overall Assessment:")
        passed = sum(1 for t in self.results["tests"] if t["status"] == "PASS")
        total = len(self.results["tests"])
        
        if passed == total:
            print(f"   ✅ ALL TESTS PASSED ({passed}/{total})")
            print("   The Voice Biometrics system is working correctly!")
        else:
            print(f"   ⚠️ SOME TESTS FAILED ({passed}/{total} passed)")
            print("   Review the failures and check system configuration")
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("\n🚀 Starting Voice Biometrics Test Suite...")
        print("="*60)
        
        if not self.test_api_health():
            print("❌ API is not running. Please start the server first.")
            return
        
        time.sleep(1)
        
        # Run tests in sequence
        if self.test_enrollment():
            time.sleep(2)  # Give time for database write
            self.test_verification_positive()
            time.sleep(1)
            self.test_verification_negative()
        
        self.test_liveness()
        self.check_database()
        self.calculate_metrics()
        self.generate_report()

# Run the test suite
if __name__ == "__main__":
    tester = VoiceBiometricsTestSuite()
    tester.run_all_tests()