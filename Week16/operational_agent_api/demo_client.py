import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(name, method, url, payload=None):
    print(f"\n--- Testing {name} ---")
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=payload, timeout=30) # Longer timeout for agent
        
        print(f"Status: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
            
    except Exception as e:
        print(f"FAILED: {e}")

# 1. Health
test_endpoint("Health Check", "GET", f"{BASE_URL}/health")

# 2. Rule-based Chat
test_endpoint("Rule-based Chat (Status)", "POST", f"{BASE_URL}/chat", {"query": "What is the system status?"})

# 3. Agent-based Chat
test_endpoint("Agent Chat (General Query)", "POST", f"{BASE_URL}/chat", {"query": "Tell me a short joke about programming."})
