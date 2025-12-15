# Network Traffic Analysis Guide

This guide explains how to use network analysis tools (Wireshark, Burp Suite, etc.) to demonstrate that sensitive data is being transmitted without encryption.

## Why Network Analysis is Important

Network traffic analysis is the **most direct way** to prove that sensitive data is being transmitted without encryption. It shows:

1. **Data in transit** - What's actually being sent over the network
2. **Lack of encryption** - Whether data is protected or not
3. **Real-world impact** - How attackers could intercept data

## Tools for Network Analysis

### 1. Wireshark (Recommended)

**Wireshark** is a free, open-source network protocol analyzer that can capture and inspect network traffic.

#### Installation

- **Windows:** Download from https://www.wireshark.org/download.html
- **Linux:** `sudo apt-get install wireshark` (Ubuntu/Debian)
- **Mac:** `brew install wireshark` or download from website

#### Basic Usage

1. **Start Wireshark:**
   - Open Wireshark
   - Select your network interface (usually "Ethernet" or "Wi-Fi")
   - Click the blue shark fin icon to start capturing

2. **Filter for relevant traffic:**
   ```
   # Filter for HTTP traffic
   http
   
   # Filter for HTTPS/TLS traffic
   tls
   
   # Filter for traffic to/from localhost:8000
   tcp.port == 8000
   
   # Combine filters
   (http or tls) and tcp.port == 8000
   ```

3. **Capture traffic while making requests:**
   ```bash
   # In another terminal, make API requests
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@university.edu", "password": "admin123"}'
   ```

4. **Analyze captured packets:**
   - Find the HTTP POST request to `/api/v1/auth/login`
   - Right-click → "Follow" → "HTTP Stream"
   - You'll see the request with password in plaintext
   - You'll see the response (may contain sensitive data)

#### Example: Capturing Login Request

**Request (visible in Wireshark):**
```
POST /api/v1/auth/login HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Content-Length: 58

{"email": "admin@university.edu", "password": "admin123"}
```

**Response (visible in Wireshark):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "admin@university.edu",
    "role": "admin"
  }
}
```

#### Example: Capturing User Data

```bash
# Make request to get all users
curl http://localhost:8000/api/v1/auth/users
```

**Response (visible in Wireshark):**
```json
[
  {
    "id": 1,
    "email": "admin@university.edu",
    "password_hash": "0192023a7bbd73250516f069df18b500",  // VULNERABLE: Visible in network traffic
    "role": "admin",
    "student_id": null,
    "last_login": "2025-12-15T10:30:00",
    "created_at": "2025-01-01T00:00:00"
  }
]
```

### 2. Burp Suite

**Burp Suite** is a web application security testing tool that includes a proxy for intercepting HTTP/HTTPS traffic.

#### Installation

- Download Community Edition (free) from: https://portswigger.net/burp/communitydownload

#### Basic Usage

1. **Start Burp Suite:**
   - Launch Burp Suite
   - Accept default project settings
   - Go to Proxy → Options
   - Note the proxy listener (usually `127.0.0.1:8080`)

2. **Configure browser/client to use proxy:**
   ```bash
   # Use Burp as proxy for curl
   curl -x http://127.0.0.1:8080 \
     -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@university.edu", "password": "admin123"}'
   ```

3. **View intercepted traffic:**
   - Go to Proxy → HTTP history
   - Click on requests to see full request/response
   - Sensitive data will be visible in plaintext

4. **Intercept and modify requests:**
   - Go to Proxy → Intercept
   - Turn intercept on
   - Requests will pause for inspection/modification
   - Click "Forward" to continue

### 3. tcpdump (Linux/Mac)

**tcpdump** is a command-line packet analyzer available on Unix-like systems.

#### Basic Usage

```bash
# Capture HTTP traffic on port 8000
sudo tcpdump -i any -A -s 0 'tcp port 8000 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'

# Save to file for later analysis
sudo tcpdump -i any -w capture.pcap 'tcp port 8000'

# Read from file
tcpdump -r capture.pcap -A
```

### 4. Python Scripts for Demonstration

Create a simple script to show what's being transmitted:

```python
#!/usr/bin/env python3
"""
Demonstrate sensitive data transmission
Shows what data is visible in network traffic
"""
import requests
import json

def demonstrate_data_exposure():
    print("=" * 70)
    print("Demonstrating Sensitive Data Transmission")
    print("=" * 70)
    print()
    
    # VULNERABLE: Login request - password transmitted in plaintext
    print("1. LOGIN REQUEST (Password in Request Body)")
    print("-" * 70)
    login_data = {
        "email": "admin@university.edu",
        "password": "admin123"  # VULNERABLE: Visible in network traffic
    }
    print(f"Request URL: http://localhost:8000/api/v1/auth/login")
    print(f"Request Body: {json.dumps(login_data, indent=2)}")
    print("⚠️  This data is visible in network traffic (Wireshark/Burp)")
    print()
    
    response = requests.post(
        'http://localhost:8000/api/v1/auth/login',
        json=login_data
    )
    
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    print()
    
    # VULNERABLE: Get users - password hashes in response
    print("2. GET USERS REQUEST (Password Hashes in Response)")
    print("-" * 70)
    print("Request URL: http://localhost:8000/api/v1/auth/users")
    print()
    
    users_response = requests.get('http://localhost:8000/api/v1/auth/users')
    users_data = users_response.json()
    
    print(f"Response Status: {users_response.status_code}")
    print(f"Response Body (first user):")
    if users_data:
        print(json.dumps(users_data[0], indent=2))
        print(f"⚠️  Password hash '{users_data[0].get('password_hash')}' is visible in network traffic")
    print()
    
    print("=" * 70)
    print("VULNERABILITY SUMMARY")
    print("=" * 70)
    print("✓ Passwords transmitted in plaintext (HTTP request body)")
    print("✓ Password hashes transmitted in plaintext (HTTP response body)")
    print("✓ All data visible to anyone monitoring network traffic")
    print("✓ No encryption protection for sensitive data")
    print()

if __name__ == "__main__":
    demonstrate_data_exposure()
```

## Step-by-Step Demonstration

### Scenario: Intercepting Login Credentials (HTTP Mode - Recommended)

**IMPORTANT FOR WINDOWS:** See `WIRESHARK_LOCALHOST_GUIDE.md` for detailed Windows-specific instructions.

1. **Start the backend on HTTP (unencrypted):**
   ```powershell
   cd backend
   $env:USE_HTTP="true"
   python main.py
   ```
   Or:
   ```powershell
   cd backend
   python main.py --http
   ```
   This runs the server on `http://localhost:8000` with **no encryption**.
   **Verify:** You should see `[!] VULNERABLE: Running on HTTP (unencrypted)` in console

2. **Install/Verify Npcap with Loopback Support (Windows):**
   - Download from: https://npcap.com/download/
   - **CRITICAL:** During installation, check "Support loopback traffic"
   - Restart Wireshark after installation

3. **Start Wireshark (as Administrator):**
   - Right-click Wireshark → Run as Administrator
   - Look for interface: **"Npcap Loopback Adapter"** or **"Adapter for loopback traffic capture"**
   - If not available, use your main network interface (Ethernet/Wi-Fi)
   - Click blue shark fin icon to start capturing

4. **Set Filter:**
   - In filter box, type: `http and tcp.port == 8000`
   - Press Enter
   - This filters for HTTP traffic on port 8000

5. **Make login request:**
   ```powershell
   curl -X POST http://localhost:8000/api/v1/auth/login `
     -H "Content-Type: application/json" `
     -d '{\"email\": \"admin@university.edu\", \"password\": \"admin123\"}'
   ```
   Or use the demo script:
   ```powershell
   cd backend
   python demonstrate_network_exposure.py
   ```

6. **In Wireshark:**
   - Look for packets with "HTTP" in Protocol column
   - Find packet with "POST /api/v1/auth/login" in Info column
   - Right-click on that packet
   - Select: **Follow → HTTP Stream**
   - A new window opens showing the HTTP conversation

7. **View the Plaintext Password:**
   - In the HTTP Stream window, you'll see:
     - **Red text (request):** Contains the password in JSON
     - **Blue text (response):** Contains the server response
   - Look for: `"password": "admin123"` in the request body

8. **Document the vulnerability:**
   - Take screenshot of Wireshark showing password
   - Show that data is transmitted without encryption
   - Explain the security impact

### Troubleshooting: Can't See HTTP Packets?

**If you don't see any HTTP packets:**

1. **Check backend is running on HTTP:**
   - Console should show: `Running on HTTP (unencrypted)`
   - Not: `Running on HTTPS`

2. **Try different filter:**
   ```
   tcp.port == 8000
   ```
   This shows all TCP traffic on port 8000

3. **Check if packets are being captured:**
   - Remove all filters temporarily
   - Make a request
   - Do you see ANY packets? If no, interface selection is wrong

4. **Try RawCap (Windows alternative):**
   - Download: https://www.netresec.com/?page=RawCap
   - Run: `RawCap.exe 127.0.0.1 capture.pcap` (as Admin)
   - Make requests
   - Open capture.pcap in Wireshark

5. **Use browser DevTools as alternative:**
   - F12 → Network tab
   - Make login request
   - Click on the request → see Headers/Payload
   - Shows request body with password (but not as detailed as Wireshark)

### Scenario: Intercepting Password Hashes

1. **Start Wireshark:**
   - Same as above

2. **Make request to get users:**
   ```bash
   curl http://localhost:8000/api/v1/auth/users
   ```

3. **In Wireshark:**
   - Find the GET request
   - Follow HTTP stream
   - Observe password hashes in response

4. **Document the vulnerability:**
   - Show password hashes in network traffic
   - Explain that even hashed data shouldn't be exposed
   - Show how this enables offline attacks

## HTTPS vs HTTP

### HTTP (Completely Unencrypted)
- All data visible in plaintext
- Easy to intercept with any network tool
- **This is what we're demonstrating**

### HTTPS with Misconfigured Certificate
- Data is encrypted, but certificate warnings allow interception
- Attackers can use man-in-the-middle attacks
- Users may accept invalid certificates
- **Still vulnerable** - demonstrates certificate misconfiguration

## Best Practices for Testing

1. **Use multiple tools:**
   - Wireshark for packet-level analysis
   - Burp Suite for web application testing
   - Python scripts for automation

2. **Document everything:**
   - Screenshots of captured traffic
   - Packet captures saved to files
   - Clear explanation of what's being exposed

3. **Show real-world impact:**
   - Demonstrate how easy it is to intercept
   - Show what an attacker could do with the data
   - Explain the security implications

## Files to Save

- **Packet captures:** Save as `.pcap` files for later analysis
- **Screenshots:** Document visible sensitive data
- **Traffic dumps:** Save HTTP streams for documentation

## Notes

- Network analysis tools are essential for demonstrating data exposure
- Shows the "real-world" vulnerability - what attackers actually see
- Complements API testing and log analysis
- Required for comprehensive security assessment


