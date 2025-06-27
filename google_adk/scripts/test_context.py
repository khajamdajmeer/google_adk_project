
import urllib.request
import json
import jwt
import time

# Configuration
URL = "http://127.0.0.1:8000/status_check"
SECRET = "your-secret-key"
ALGORITHM = "HS256"

def generate_token():
    payload = {
        "sub": "user123",
        "name": "Test User",
        "role": "admin",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token, payload

def test_context():
    print(f"Testing {URL}...")
    token, payload = generate_token()
    print(f"Generated Token: {token}")
    
    headers = {
        "authtoken": token
    }
    
    req = urllib.request.Request(URL, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print(f"Failed with status: {response.status}")
                return
            
            data = json.loads(response.read().decode())
            print("Response:", json.dumps(data, indent=2))
            
            context = data.get("status", {}).get("request_context", {})
            
            if context.get("sub") == payload["sub"]:
                print("\nSUCCESS: Request context populated correctly!")
            else:
                print("\nFAILURE: Request context missing or incorrect.")
                
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure the server is running: uvicorn app.main:app --reload")

if __name__ == "__main__":
    test_context()
