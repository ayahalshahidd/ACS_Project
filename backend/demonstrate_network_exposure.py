#!/usr/bin/env python3
"""
Demonstration script for network traffic analysis
Shows what sensitive data is visible in network traffic
"""
import requests
import json

def demonstrate_data_exposure():
    """
    Demonstrate that sensitive data is transmitted without encryption
    This shows what would be visible in Wireshark/Burp Suite
    """
    print("=" * 70)
    print("Network Traffic Analysis Demonstration")
    print("Sensitive Data Exposure - What's Visible in Network Traffic")
    print("=" * 70)
    print()
    print("IMPORTANT: For easiest network analysis, run the backend on HTTP:")
    print("  USE_HTTP=true python main.py")
    print("  This runs on http://localhost:8000 (unencrypted)")
    print("  All data will be visible in plaintext in Wireshark")
    print()
    
    # VULNERABLE: Login request - password transmitted in plaintext
    print("1. LOGIN REQUEST (Password Visible in Network Traffic)")
    print("-" * 70)
    login_data = {
        "email": "admin@university.edu",
        "password": "admin123"  # VULNERABLE: Visible in Wireshark/Burp
    }
    print(f"Request URL: http://localhost:8000/api/v1/auth/login")
    print(f"Request Method: POST")
    print(f"Request Headers:")
    print(f"  Content-Type: application/json")
    print(f"Request Body (visible in network traffic):")
    print(f"  {json.dumps(login_data, indent=2)}")
    print()
    print("⚠️  VULNERABILITY: Password is transmitted in PLAINTEXT")
    print("   - Visible in Wireshark packet capture")
    print("   - Visible in Burp Suite HTTP history")
    print("   - Anyone monitoring network can see the password")
    print()
    
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            json=login_data,
            timeout=5
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Body (visible in network traffic):")
        print(f"  {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not connect to server: {e}")
        print("   Make sure the backend is running: python main.py")
    print()
    print()
    
    # VULNERABLE: Get users - password hashes in response
    print("2. GET USERS REQUEST (Password Hashes Visible in Network Traffic)")
    print("-" * 70)
    print("Request URL: http://localhost:8000/api/v1/auth/users")
    print("Request Method: GET")
    print()
    
    try:
        users_response = requests.get('http://localhost:8000/api/v1/auth/users', timeout=5)
        users_data = users_response.json()
        
        print(f"Response Status: {users_response.status_code}")
        print(f"Response Body (visible in network traffic):")
        if users_data and len(users_data) > 0:
            print(f"  First user data:")
            print(f"  {json.dumps(users_data[0], indent=2)}")
            print()
            print("⚠️  VULNERABILITY: Password hash is transmitted in PLAINTEXT")
            print(f"   - Hash: {users_data[0].get('password_hash', 'N/A')}")
            print("   - Visible in Wireshark packet capture")
            print("   - Visible in Burp Suite HTTP history")
            print("   - Can be cracked using rainbow tables or brute force")
        else:
            print("  No users found")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not connect to server: {e}")
        print("   Make sure the backend is running: python main.py")
    print()
    print()
    
    # VULNERABLE: User registration - password and hash exposed
    print("3. USER REGISTRATION (Password and Hash Visible in Network Traffic)")
    print("-" * 70)
    print("Request URL: http://localhost:8000/api/v1/auth/register")
    print("Request Method: POST")
    print("Request Parameters (visible in URL or body):")
    print("  email: test@example.com")
    print("  password: MySecretPassword123  # VULNERABLE: Visible in network")
    print()
    
    try:
        reg_response = requests.post(
            'http://localhost:8000/api/v1/auth/register',
            params={
                'email': 'test@example.com',
                'password': 'MySecretPassword123',
                'role': 'student'
            },
            timeout=5
        )
        
        print(f"Response Status: {reg_response.status_code}")
        if reg_response.status_code == 200:
            reg_data = reg_response.json()
            print(f"Response Body (visible in network traffic):")
            print(f"  {json.dumps(reg_data, indent=2)}")
            print()
            print("⚠️  VULNERABILITY: Password hash returned in response")
            print("   - Both password (in request) and hash (in response) visible")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not connect to server: {e}")
    print()
    print()
    
    print("=" * 70)
    print("VULNERABILITY SUMMARY")
    print("=" * 70)
    print("✓ Passwords transmitted in plaintext (HTTP request body)")
    print("✓ Password hashes transmitted in plaintext (HTTP response body)")
    print("✓ All data visible to anyone monitoring network traffic")
    print("✓ No encryption protection for sensitive data")
    print()
    print("HOW TO VERIFY WITH WIRESHARK:")
    print("1. Start backend on HTTP: USE_HTTP=true python main.py")
    print("2. Start Wireshark and capture traffic on port 8000")
    print("3. Filter: http and tcp.port == 8000")
    print("4. Run this script or make curl requests")
    print("5. In Wireshark: Right-click POST request → Follow → HTTP Stream")
    print("6. Observe: All sensitive data visible in plaintext")
    print()
    print("Note: If using HTTPS, you need to decrypt TLS traffic (see NETWORK_ANALYSIS_GUIDE.md)")
    print("      HTTP mode is recommended for easiest demonstration")
    print()
    print("See NETWORK_ANALYSIS_GUIDE.md for detailed instructions")
    print()

if __name__ == "__main__":
    demonstrate_data_exposure()


