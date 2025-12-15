# Testing Data Exposure Vulnerabilities

This guide explains how to test and demonstrate the data exposure vulnerabilities where sensitive data is stored or transmitted without encryption.

## Data Exposure Vulnerabilities

The application has multiple instances of sensitive data exposure:

1. **Password Hashes Exposed in API Responses**
2. **Passwords Logged in Plaintext**
3. **Error Messages Expose Sensitive Information**
4. **System Information Exposure**
5. **User Data Export Without Protection**

## Testing Methods

### 0. Network Traffic Analysis

**EASIEST METHOD: Browser DevTools (Recommended - No Setup Required!)**

See `BROWSER_DEVTOOLS_GUIDE.md` for the simplest method using browser DevTools.

**ADVANCED METHOD: Wireshark/Burp Suite**

For packet-level analysis, see `WIRESHARK_LOCALHOST_GUIDE.md` for detailed instructions.

#### Quick Browser DevTools Method (Easiest!)

1. **Start backend on HTTP:**
   ```powershell
   cd backend
   USE_HTTP=true python main.py
   ```

2. **Open browser DevTools:**
   - Go to `http://localhost:3000`
   - Press `F12` → Network tab
   - Check "Preserve log"

3. **Make login request** (use login form or console)

4. **View request:**
   - Click on `/api/v1/auth/login` request
   - Go to "Payload" tab
   - **Password visible in plaintext!**

**See `BROWSER_DEVTOOLS_GUIDE.md` for full instructions.**

#### Option A: Run Backend on HTTP (For Wireshark Analysis)

For easiest network analysis, run the backend on HTTP (unencrypted):

```bash
cd backend

# Run on HTTP (unencrypted) - easiest for Wireshark analysis
USE_HTTP=true python main.py

# Or use command line flag
python main.py --http
```

This will run the server on `http://localhost:8000` with **no encryption** - all data is transmitted in plaintext.

#### Option B: Use HTTPS with Misconfigured Certificate

The backend runs on HTTPS by default, but the certificate is misconfigured. See `HTTPS_TESTING_GUIDE.md` for detailed instructions.

**Quick HTTPS Testing:**

1. **Start backend on HTTPS:**
   ```powershell
   cd backend
   python main.py  # Runs on HTTPS by default
   ```

2. **Use Browser DevTools (works with HTTPS!):**
   - DevTools shows data before encryption (client-side)
   - Go to `http://localhost:3000` → F12 → Network tab
   - Make requests - data is visible even with HTTPS!

3. **For Wireshark with HTTPS:**
   - Configure TLS decryption (see `HTTPS_TESTING_GUIDE.md`)
   - Use private key to decrypt traffic
   - Demonstrates that misconfigured certificates allow interception

4. **Use Burp Suite:**
   - Easily intercepts HTTPS traffic
   - Shows plaintext request/response

#### Using Wireshark with HTTP (Easiest)

1. **Install Wireshark:**
   - Download from: https://www.wireshark.org/
   - Install on your system

2. **Start the backend on HTTP:**
   ```bash
   cd backend
   USE_HTTP=true python main.py
   ```

3. **Start capturing traffic:**
   - Open Wireshark
   - Select your network interface (usually "Ethernet" or "Wi-Fi")
   - Click "Start capturing packets"

4. **Filter for HTTP traffic:**
   - In the filter box, type: `http and tcp.port == 8000`
   - This will show only HTTP traffic on port 8000

5. **Make API requests while capturing:**
   ```bash
   # Make a login request (will transmit password in plaintext)
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@university.edu", "password": "admin123"}'
   
   # Get users (will transmit password hashes in plaintext)
   curl http://localhost:8000/api/v1/auth/users
   ```

6. **Analyze captured packets:**
   - Look for HTTP POST requests to `/api/v1/auth/login`
   - Right-click → "Follow" → "HTTP Stream"
   - You should see the password in **plaintext** in the request body
   - You should see password hashes in **plaintext** in the response

**Expected Result:**
- Passwords visible in HTTP request bodies (plaintext)
- Password hashes visible in HTTP responses (plaintext)
- All data completely unencrypted and visible

#### Using Wireshark with HTTPS (Misconfigured Certificate)

If using HTTPS, you can decrypt the traffic:

1. **Start the backend on HTTPS:**
   ```bash
   cd backend
   python main.py  # Runs on HTTPS by default
   ```

2. **Configure Wireshark to decrypt TLS:**
   - Go to Edit → Preferences → Protocols → TLS
   - Add the private key: Click "RSA keys list" → Edit → Add
   - IP address: `127.0.0.1`
   - Port: `8000`
   - Protocol: `http`
   - Key file: Browse to `backend/key.pem`

3. **Capture and analyze:**
   - Filter: `tls and tcp.port == 8000`
   - Make requests
   - Right-click → "Follow" → "TLS Stream"
   - Decrypted data will be visible

**Note:** The misconfigured certificate makes this easier, but HTTPS traffic is still encrypted. For easiest demonstration, use HTTP mode.

#### Using Burp Suite

1. **Install Burp Suite Community Edition:**
   - Download from: https://portswigger.net/burp/communitydownload

2. **Configure proxy:**
   - Start Burp Suite
   - Go to Proxy → Options
   - Note the proxy address (usually `127.0.0.1:8080`)

3. **Configure your client:**
   ```bash
   # Use Burp as proxy
   curl -x http://127.0.0.1:8080 -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@university.edu", "password": "admin123"}'
   ```

4. **View intercepted traffic:**
   - Go to Proxy → HTTP history
   - Click on requests to see request/response
   - Sensitive data will be visible in plaintext

#### Using tcpdump (Linux/Mac)

```bash
# Capture HTTP traffic on port 8000
sudo tcpdump -i any -A -s 0 'tcp port 8000 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'

# Make requests while capturing
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@university.edu", "password": "admin123"}'
```

#### Using Python to demonstrate network interception

Create a simple script to show data transmission:

```python
import requests
import json

# VULNERABLE: Data transmitted without encryption (HTTP)
response = requests.post(
    'http://localhost:8000/api/v1/auth/login',
    json={'email': 'admin@university.edu', 'password': 'admin123'}
)

print("Request sent (visible in network traffic):")
print(f"  URL: {response.request.url}")
print(f"  Body: {response.request.body}")  # Password visible here
print(f"\nResponse received (visible in network traffic):")
print(f"  Status: {response.status_code}")
print(f"  Body: {json.dumps(response.json(), indent=2)}")  # May contain sensitive data
```

**Key Points:**
- Even with HTTPS, misconfigured certificates allow interception
- HTTP traffic is completely unencrypted
- Network sniffing tools can capture all data
- Demonstrates the vulnerability of transmitting sensitive data without proper encryption

### 1. Password Hashes Exposed in API Responses

#### Test: Get All Users (Exposes Password Hashes)

```bash
# Get all users - exposes password hashes
curl https://localhost:8000/api/v1/auth/users

# Get specific user - exposes password hash
curl https://localhost:8000/api/v1/auth/users/1
```

**Expected Result:**
- API returns user data including `password_hash` field
- Password hashes are visible in the response
- No authentication or authorization required

**Vulnerability:**
- Password hashes should never be exposed in API responses
- Even hashed passwords can be cracked (especially MD5)
- Should require admin authentication

#### Test: User Registration (Exposes Password Hash)

```bash
curl -X POST "https://localhost:8000/api/v1/auth/register?email=test@example.com&password=secret123&role=student"
```

**Expected Result:**
- Response includes `password_hash` field
- Password hash is visible in the response

### 2. Passwords Logged in Plaintext

#### Test: Login with Password Logging

1. **Start the backend server:**
   ```bash
   cd backend
   python main.py
   ```

2. **Make a login request:**
   ```bash
   curl -X POST https://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@university.edu", "password": "admin123"}'
   ```

3. **Check the server logs:**
   - Look for log entries containing: `Login attempt for email: ..., password: ...`
   - Password is logged in plaintext

**Vulnerability:**
- Passwords should never be logged
- Logs may be stored, backed up, or accessed by unauthorized users
- Logs can be used to compromise user accounts

#### Test: User Registration with Password Logging

```bash
curl -X POST "https://localhost:8000/api/v1/auth/register?email=newuser@example.com&password=MySecretPassword123"
```

**Check logs for:**
- `User registration attempt: email=..., password=...`
- Password logged in plaintext

### 3. Error Messages Expose Sensitive Information

#### Test: Database Error Information Disclosure

```bash
# Try to access non-existent course with invalid ID
curl https://localhost:8000/api/v1/courses/99999

# Try to access non-existent user
curl https://localhost:8000/api/v1/auth/users/99999
```

**Expected Result:**
- Error messages reveal:
  - Database table names (`courses table`, `users table`)
  - Query details
  - Database structure
  - Internal IDs

**Vulnerability:**
- Error messages should be generic
- Should not expose database structure or query details
- Can help attackers understand the system architecture

#### Test: Login Error Information Disclosure

```bash
curl -X POST https://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "nonexistent@example.com", "password": "wrong"}'
```

**Expected Result:**
- Error message includes email address
- Reveals whether user exists or not

### 4. System Information Exposure

#### Test: Debug Info Endpoint

```bash
# Get system information (exposes sensitive data)
curl https://localhost:8000/api/v1/debug/info
```

**Expected Result:**
- Returns:
  - Environment variables (including secrets if any)
  - Database connection string (with credentials)
  - System paths and file locations
  - Python version and platform information

**Vulnerability:**
- Should never be enabled in production
- Exposes system configuration
- Can reveal secrets and credentials
- Helps attackers understand the infrastructure

### 5. User Data Export Without Protection

#### Test: Export All Users

```bash
# Export all user data (no authentication required)
curl https://localhost:8000/api/v1/debug/users/export
```

**Expected Result:**
- Returns all user data including:
  - Email addresses
  - Password hashes
  - Student IDs (PII)
  - Last login times
  - Account creation dates

**Vulnerability:**
- Should require admin authentication
- Should not expose password hashes
- Should not expose PII without proper authorization
- Violates data protection regulations (GDPR, etc.)

## Security Impact

### Why These Exposures Are Vulnerable:

1. **Password Hash Exposure:**
   - Even hashed passwords can be cracked (especially MD5)
   - Attackers can use rainbow tables
   - Enables offline password attacks
   - Users often reuse passwords across services

2. **Plaintext Password Logging:**
   - Logs may be stored insecurely
   - Logs can be accessed by unauthorized users
   - Logs may be backed up or archived
   - Immediate compromise if logs are leaked

3. **Error Message Information Disclosure:**
   - Reveals system architecture
   - Helps attackers understand database structure
   - Can be used for further attacks (SQL injection, etc.)
   - Violates principle of least information

4. **System Information Exposure:**
   - Reveals infrastructure details
   - Can expose secrets and credentials
   - Helps attackers plan attacks
   - Should never be accessible in production

5. **Unprotected Data Export:**
   - Violates data protection regulations
   - Enables mass data breaches
   - No audit trail
   - Can lead to identity theft

## Demonstration for Security Assessment

To demonstrate these vulnerabilities:

1. **Document the exposures:**
   - Show API responses with password hashes
   - Show log files with plaintext passwords
   - Show error messages with sensitive information
   - Show debug endpoint responses

2. **Demonstrate the impact:**
   - Show how password hashes can be cracked
   - Show how logs can be accessed
   - Show how error messages help attackers
   - Show how system info can be exploited

3. **Recommended Fixes:**
   - Never expose password hashes in API responses
   - Never log passwords or sensitive data
   - Use generic error messages
   - Disable debug endpoints in production
   - Implement proper authentication and authorization
   - Encrypt sensitive data at rest and in transit
   - Follow data protection regulations (GDPR, etc.)

## Testing Checklist

- [ ] **Network Traffic Analysis:**
  - [ ] Captured login request with Wireshark - password visible in plaintext
  - [ ] Captured API response with Wireshark - password hash visible in plaintext
  - [ ] Used Burp Suite to intercept and view sensitive data
  - [ ] Demonstrated that HTTP traffic is completely unencrypted
  - [ ] Demonstrated that HTTPS with misconfigured cert can be intercepted
- [ ] Password hashes exposed in `/api/v1/auth/users` endpoint
- [ ] Password hashes exposed in `/api/v1/auth/users/{id}` endpoint
- [ ] Passwords logged in plaintext during login
- [ ] Passwords logged in plaintext during registration
- [ ] Error messages expose database structure
- [ ] Error messages expose query details
- [ ] System information exposed in `/api/v1/debug/info`
- [ ] User data export accessible without authentication
- [ ] Sensitive data transmitted without encryption (verified with network tools)

## Network Traffic Analysis

**IMPORTANT:** Use network analysis tools (Wireshark, Burp Suite) to demonstrate that sensitive data is transmitted without encryption. See `NETWORK_ANALYSIS_GUIDE.md` for detailed instructions.

### Quick Test with Wireshark:

**For detailed Windows instructions, see `WIRESHARK_LOCALHOST_GUIDE.md`**

**Quick Steps:**

1. **Install Npcap with loopback support** (Windows):
   - Download: https://npcap.com/download/
   - **IMPORTANT:** Check "Support loopback traffic" during installation

2. **Start backend on HTTP:**
   ```powershell
   cd backend
   USE_HTTP=true python main.py
   ```

3. **Start Wireshark (as Administrator):**
   - Select "Npcap Loopback Adapter" interface
   - Filter: `http and tcp.port == 8000`
   - Start capturing

4. **Make login request:**
   ```powershell
   curl -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\": \"admin@university.edu\", \"password\": \"admin123\"}"
   ```

5. **In Wireshark:**
   - Find packet with "POST /api/v1/auth/login"
   - Right-click → Follow → HTTP Stream
   - Observe: Password is visible in plaintext in the request body

**If you can't see HTTP packets, see `WIRESHARK_LOCALHOST_GUIDE.md` for troubleshooting.**

This is the **most direct proof** that sensitive data is transmitted without encryption.

## Notes

- These vulnerabilities are intentional for security testing/education
- **Network traffic analysis is essential** to demonstrate data exposure
- Use Wireshark, Burp Suite, or similar tools to capture and analyze traffic
- In production, always:
  - Encrypt sensitive data in transit (HTTPS with valid certificates)
  - Encrypt sensitive data at rest
  - Never log passwords
  - Use generic error messages
  - Disable debug endpoints in production
  - Implement proper access controls
  - Follow data protection best practices
- Data exposure is a common security issue in real-world applications


