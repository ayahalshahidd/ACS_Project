#!/usr/bin/env python3
"""
Test script to verify Wireshark can capture HTTP traffic
This makes simple requests to help you find them in Wireshark
"""
import requests
import time
import sys

def test_wireshark_capture():
    """
    Make test requests that should be visible in Wireshark
    """
    base_url = "http://localhost:8000"
    
    print("=" * 70)
    print("Wireshark Capture Test")
    print("=" * 70)
    print()
    print("This script will make HTTP requests that should be visible in Wireshark")
    print("Make sure:")
    print("  1. Backend is running: USE_HTTP=true python main.py")
    print("  2. Wireshark is capturing on loopback interface")
    print("  3. Filter is set: http and tcp.port == 8000")
    print()
    
    input("Press ENTER when Wireshark is ready and capturing...")
    print()
    
    try:
        # Test 1: Simple GET request (easy to find)
        print("[TEST 1] Making GET request to /health endpoint...")
        print(f"  URL: {base_url}/health")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        print("  ✓ Look for 'GET /health HTTP/1.1' in Wireshark")
        print()
        time.sleep(2)
        
        # Test 2: Login request with password
        print("[TEST 2] Making POST request to /api/v1/auth/login...")
        print(f"  URL: {base_url}/api/v1/auth/login")
        print("  Body: {\"email\": \"admin@university.edu\", \"password\": \"admin123\"}")
        login_data = {
            "email": "admin@university.edu",
            "password": "admin123"
        }
        response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json=login_data,
            timeout=5
        )
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        print("  ✓ Look for 'POST /api/v1/auth/login HTTP/1.1' in Wireshark")
        print("  ✓ Password should be visible in request body")
        print()
        time.sleep(2)
        
        # Test 3: Get users (password hashes)
        print("[TEST 3] Making GET request to /api/v1/auth/users...")
        print(f"  URL: {base_url}/api/v1/auth/users")
        response = requests.get(f"{base_url}/api/v1/auth/users", timeout=5)
        print(f"  Status: {response.status_code}")
        users = response.json()
        if users:
            print(f"  Found {len(users)} users")
            print(f"  First user email: {users[0].get('email')}")
            print(f"  Password hash: {users[0].get('password_hash')}")
        print("  ✓ Look for 'GET /api/v1/auth/users HTTP/1.1' in Wireshark")
        print("  ✓ Password hash should be visible in response")
        print()
        
        print("=" * 70)
        print("TESTS COMPLETE")
        print("=" * 70)
        print()
        print("In Wireshark:")
        print("  1. Look for packets with 'HTTP' in Protocol column")
        print("  2. Find packets with 'GET /health' or 'POST /api/v1/auth/login' in Info column")
        print("  3. Right-click on a packet → Follow → HTTP Stream")
        print("  4. You should see the request/response in plaintext")
        print()
        print("If you don't see HTTP packets:")
        print("  - Check filter: http and tcp.port == 8000")
        print("  - Try filter: tcp.port == 8000 (to see all TCP traffic)")
        print("  - Make sure backend is running on HTTP (not HTTPS)")
        print("  - Check WIRESHARK_LOCALHOST_GUIDE.md for troubleshooting")
        print()
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to backend")
        print("Make sure backend is running:")
        print("  cd backend")
        print("  USE_HTTP=true python main.py")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_wireshark_capture()

