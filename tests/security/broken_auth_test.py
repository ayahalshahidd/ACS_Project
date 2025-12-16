import pytest
import requests
import urllib3

# Suppress SSL warnings (if running locally without certs)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CONFIGURATION
BASE_URL = "http://localhost:8000/api/v1"

def test_hardcoded_backdoor_exploit():
    """
    Test: Attempt to access an Admin endpoint using only the secret header.
    
    VULNERABLE: Server returns 200/201 (Backdoor works).
    SECURE:     Server returns 401/403 (Unauthorized).
    """
    
    # 1. The Malicious Header (The "Key")
    backdoor_headers = {
        "X-Admin-Access": "SuperSecretAdmin123",
        "Content-Type": "application/json"
    }
    
    # 2. The Payload (Using Lists/Dicts to avoid 500 errors)
    payload = {
        "code": "SEC-TEST-999",
        "title": "Backdoor Verification Test",
        "capacity": 1,
        "instructor_id": 1,  # Links to existing admin to prevent orphan crash
        "prereq_ids": [],
        "schedule": {}
    }
    
    # 3. Launch Attack
    # We use a raw requests.post (not a session) to prove we have NO cookies/login.
    response = requests.post(
        f"{BASE_URL}/admin/courses",
        json=payload,
        headers=backdoor_headers,
        verify=False
    )
    
    # 4. Assert System Security
    # If response is 200, the Assertion FAILS -> Vulnerability Found.
    # If response is 401/403, the Assertion PASSES -> System Secure.
    assert response.status_code in [401, 403], \
        f"VULNERABILITY DETECTED: Backdoor is active! Expected 401/403, but got {response.status_code}. Course created."