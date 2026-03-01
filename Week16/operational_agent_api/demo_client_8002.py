import requests
import json

BASE_URL = "http://127.0.0.1:8002"

print(f"Testing against {BASE_URL}...")

# 1. Health
print("1. Checking Health...")
try:
    r = requests.get(f"{BASE_URL}/health")
    print(f"Health: {r.status_code} {r.json()}")
except Exception as e:
    print(f"Health Check Failed: {e}")

# 2. Agent
print("\n2. Checking Agent Path...")
try:
    payload = {"query": "Tell me a short joke about programming."}
    r = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("Success!")
        print(json.dumps(r.json(), indent=2))
    else:
        print("Failed!")
        print(r.text)
except Exception as e:
    print(f"Agent Check Failed: {e}")
