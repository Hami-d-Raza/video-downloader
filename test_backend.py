#!/usr/bin/env python3
"""
Quick test script to verify Railway backend is working
"""

import requests
import json

# Backend URL
BACKEND_URL = "https://video-downloader-production-e4fe.up.railway.app"

print("🔍 Testing Railway Backend...\n")

# Test 1: Health Check
print("1. Testing /health endpoint...")
try:
    response = requests.get(f"{BACKEND_URL}/health", timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# Test 2: Root endpoint
print("2. Testing / endpoint...")
try:
    response = requests.get(f"{BACKEND_URL}/", timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# Test 3: Analyze endpoint with YouTube URL
print("3. Testing /api/analyze endpoint...")
try:
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    response = requests.post(
        f"{BACKEND_URL}/api/analyze",
        json={"url": test_url},
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Title: {data.get('title', 'N/A')}")
        print(f"   ✅ Platform: {data.get('platform', 'N/A')}")
        print(f"   ✅ Formats: {len(data.get('formats', []))}")
    else:
        print(f"   ❌ Error Response: {response.text}\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

print("\n✅ Backend test complete!")
