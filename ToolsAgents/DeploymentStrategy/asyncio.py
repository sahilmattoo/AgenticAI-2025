## Simulate 50 Concurrent Requests

import asyncio
import httpx
import time

URL = "http://127.0.0.1:8000/chat"

payload = {
    "session_id": "load_test_user",
    "message": "My profile: 6 years Python backend experience. What roles fit?"
}

async def send_request(client, i):
    start = time.time()
    response = await client.post(URL, json=payload)
    latency = round(time.time() - start, 3)
    print(f"Request {i} → Status {response.status_code} → {latency}s")

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [send_request(client, i) for i in range(50)]
        await asyncio.gather(*tasks)

asyncio.run(main())