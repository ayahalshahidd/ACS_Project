# Testing Data Exposure with HTTPS (Misconfigured Certificate)

This guide explains how to test data exposure vulnerabilities when the backend is running on HTTPS with a misconfigured certificate.

## Why Test with HTTPS?

Even with HTTPS, the misconfigured certificate demonstrates vulnerabilities:
1. **Certificate warnings** - Users can bypass security warnings
2. **Man-in-the-middle attacks** - Misconfigured certificates allow interception
3. **Data exposure** - Shows that HTTPS alone isn't enough if certificates are misconfigured

## Method 1: Browser DevTools (Easiest - Works with HTTPS!)

Browser DevTools shows data **before encryption** (client-side), so it works perfectly with HTTPS:

### Steps:

1. **Start backend on HTTPS:**
   ```powershell
   cd backend
   python main.py  # Runs on HTTPS by default
   ```

2. **Open browser:**
   - Go to `http://localhost:3000`
   - Press `F12` → Network tab

3. **Accept certificate warning (if accessing backend directly):**
   - If you visit `https://localhost:8000` directly, browser will warn about certificate
   - Click "Advanced" → "Proceed to localhost (unsafe)"
   - This demonstrates the vulnerability - users can bypass warnings!

4. **Make requests:**
   - Use the frontend or console
   - DevTools will show the request/response data
   - **Data is visible even though it's sent over HTTPS!**

**Why this works:** Browser DevTools shows data at the application layer (before encryption), so you see the plaintext data that will be encrypted and sent over HTTPS.

## Method 2: Wireshark with TLS Decryption

To see the actual encrypted/decrypted traffic in Wireshark:

### Step 1: Start Backend on HTTPS

```powershell
cd backend
python main.py
```

### Step 2: Configure Wireshark to Decrypt TLS

1. **Open Wireshark (as Administrator)**

2. **Configure TLS Decryption:**
   - Go to: Edit → Preferences → Protocols → TLS
   - Click "RSA keys list" → Edit → Add
   - Fill in:
     - **IP address:** `127.0.0.1`
     - **Port:** `8000`
     - **Protocol:** `http`
     - **Key file:** Browse to `backend/key.pem` (the private key)
   - Click OK

3. **Start Capturing:**
   - Select appropriate interface (loopback adapter if available)
   - Filter: `tls and tcp.port == 8000`
   - Start capture

4. **Make Requests:**
   ```powershell
   # Accept certificate warning first
   curl -k -X POST https://localhost:8000/api/v1/auth/login `
     -H "Content-Type: application/json" `
     -d "{\"email\": \"admin@university.edu\", \"password\": \"admin123\"}"
   ```

5. **View Decrypted Traffic:**
   - Find TLS packets
   - Right-click → Follow → TLS Stream
   - You should see decrypted HTTP data
   - Password will be visible in the decrypted stream

**What this demonstrates:**
- HTTPS traffic is encrypted
- But with the private key, you can decrypt it
- Shows that misconfigured certificates allow interception
- Demonstrates man-in-the-middle attack scenario

## Method 3: Burp Suite (Best for HTTPS Interception)

Burp Suite can easily intercept HTTPS traffic:

### Steps:

1. **Start Backend on HTTPS:**
   ```powershell
   cd backend
   python main.py
   ```

2. **Start Burp Suite:**
   - Launch Burp Suite
   - Go to Proxy → Options
   - Note proxy address (usually `127.0.0.1:8080`)

3. **Configure Browser/Client:**
   - Install Burp's CA certificate (for HTTPS interception)
   - OR use curl with proxy:
     ```powershell
     curl -x http://127.0.0.1:8080 -k -X POST https://localhost:8000/api/v1/auth/login `
       -H "Content-Type: application/json" `
       -d "{\"email\": \"admin@university.edu\", \"password\": \"admin123\"}"
     ```

4. **View Intercepted Traffic:**
   - Go to Proxy → HTTP history
   - Click on requests
   - See request/response in plaintext
   - Sensitive data visible!

## Method 4: Demonstrate Certificate Misconfiguration

### Test 1: Browser Certificate Warning

1. **Start backend on HTTPS:**
   ```powershell
   cd backend
   python main.py
   ```

2. **Open browser to:**
   ```
   https://localhost:8000
   ```

3. **Observe certificate warnings:**
   - Chrome/Edge: "Your connection is not private"
   - Firefox: "Warning: Potential Security Risk Ahead"
   - Shows errors:
     - `NET::ERR_CERT_AUTHORITY_INVALID` (self-signed)
     - `NET::ERR_CERT_COMMON_NAME_INVALID` (wrong CN)
     - `NET::ERR_CERT_DATE_INVALID` (expired)

4. **Bypass the warning:**
   - Click "Advanced" → "Proceed to localhost (unsafe)"
   - **This demonstrates the vulnerability!**
   - Users can bypass security warnings
   - Attackers can create similar certificates

### Test 2: Certificate Details

1. **In browser, click the lock icon** (or warning icon)
2. **View certificate details:**
   - Shows: Expired certificate
   - Shows: Wrong Common Name (`wrong-domain.example.com`)
   - Shows: Self-signed certificate
3. **Take screenshot** - documents the misconfiguration

## What HTTPS Testing Demonstrates

### 1. Certificate Misconfiguration Vulnerabilities:
- ✅ Expired certificate
- ✅ Wrong Common Name
- ✅ Self-signed certificate
- ✅ Users can bypass warnings

### 2. Data Exposure (Even with HTTPS):
- ✅ Browser DevTools shows plaintext data (client-side)
- ✅ With private key, traffic can be decrypted
- ✅ Misconfigured certificates allow man-in-the-middle attacks
- ✅ Shows that HTTPS alone isn't sufficient

### 3. Real-World Impact:
- ✅ Users may accept invalid certificates
- ✅ Attackers can create similar certificates
- ✅ Man-in-the-middle attacks possible
- ✅ Data can be intercepted despite HTTPS

## Comparison: HTTP vs HTTPS Testing

### HTTP Testing:
- ✅ Easiest to demonstrate
- ✅ All traffic visible in plaintext
- ✅ No certificate setup needed
- ✅ Perfect for Wireshark analysis
- ✅ Clearly shows unencrypted data

### HTTPS Testing:
- ✅ More realistic scenario
- ✅ Demonstrates certificate misconfiguration
- ✅ Shows that HTTPS alone isn't enough
- ✅ Demonstrates man-in-the-middle vulnerability
- ✅ Shows browser warnings can be bypassed

## Recommended Approach

**For Data Exposure Demonstration:**
1. **Use HTTP** - Easiest to show unencrypted data
2. **Use Browser DevTools** - Works with both HTTP and HTTPS
3. **Document certificate misconfigurations** separately

**For Certificate Misconfiguration Demonstration:**
1. **Use HTTPS** - Shows certificate warnings
2. **Use browser** - See certificate errors
3. **Use Wireshark with TLS decryption** - Show traffic can be intercepted
4. **Use Burp Suite** - Easy HTTPS interception

## Quick Test: HTTPS with Browser DevTools

1. **Start backend:**
   ```powershell
   cd backend
   python main.py  # HTTPS mode
   ```

2. **Open browser DevTools:**
   - Go to `http://localhost:3000`
   - F12 → Network tab

3. **Make login request:**
   - Use login form or console

4. **View request:**
   - Find `/api/v1/auth/login` request
   - Click on it → Payload tab
   - **Password visible!** (even though sent over HTTPS)

5. **Check certificate:**
   - If accessing `https://localhost:8000` directly
   - Click lock/warning icon
   - View certificate details
   - **See misconfigurations!**

This demonstrates both:
- Data exposure (visible in DevTools)
- Certificate misconfiguration (browser warnings)

## Summary

**HTTPS testing is valuable because:**
- Shows certificate misconfiguration vulnerabilities
- Demonstrates that HTTPS alone isn't sufficient
- Shows how misconfigured certificates allow interception
- More realistic than pure HTTP

**But for easiest data exposure demonstration:**
- HTTP + Browser DevTools is simplest
- No certificate warnings to deal with
- Clear demonstration of unencrypted data

**Best approach:** Test both!
- Use HTTP to clearly show unencrypted data
- Use HTTPS to show certificate misconfiguration
- Both demonstrate different aspects of the vulnerabilities

