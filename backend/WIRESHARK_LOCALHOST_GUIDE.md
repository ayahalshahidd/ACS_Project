# Wireshark Localhost Capture Guide (Windows)

This guide provides detailed step-by-step instructions for capturing localhost HTTP traffic in Wireshark on Windows.

## Quick Start (TL;DR)

1. **Install Npcap with loopback support:** https://npcap.com/download/ (check "Support loopback traffic")
2. **Start backend on HTTP:** `USE_HTTP=true python main.py`
3. **Open Wireshark as Administrator**
4. **Select "Npcap Loopback Adapter" interface**
5. **Set filter:** `http and tcp.port == 8000`
6. **Start capture (blue shark fin icon)**
7. **Make request:** `curl -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\": \"admin@university.edu\", \"password\": \"admin123\"}"`
8. **In Wireshark:** Find "POST /api/v1/auth/login" packet → Right-click → Follow → HTTP Stream
9. **See password in plaintext!**

If this doesn't work, read the full guide below for troubleshooting.

## The Problem

On Windows, capturing localhost (127.0.0.1) traffic is tricky because:
- Regular network interfaces don't capture loopback traffic
- You need to use a loopback adapter or raw sockets
- Wireshark needs special configuration

## Solution: Use Npcap Loopback Adapter

### Step 1: Install/Verify Npcap with Loopback Support

1. **Download Npcap** (if not already installed):
   - Go to: https://npcap.com/download/
   - Download the latest installer
   - **IMPORTANT:** During installation, check "Install Npcap in WinPcap API-compatible Mode"
   - **CRITICAL:** Check "Support loopback traffic" - this is essential!

2. **Verify Installation:**
   - Open Wireshark → Help → About Wireshark → Plugins
   - Look for "npcap" in the list
   - OR check if you see "Npcap Loopback Adapter" in interface list
   - OR check Windows Control Panel → Programs → Look for "Npcap"

### Step 2: Configure Wireshark

1. **Open Wireshark** (as Administrator - right-click → Run as Administrator)

2. **Check Available Interfaces:**
   - Look for an interface named:
     - `Npcap Loopback Adapter`
     - `Adapter for loopback traffic capture`
     - Or similar loopback-related name
   - This interface will capture localhost traffic

3. **If you don't see a loopback adapter:**
   - Reinstall Npcap with loopback support enabled
   - Restart Wireshark

### Step 3: Start Capturing

1. **Select the Loopback Interface:**
   - Click on `Npcap Loopback Adapter` (or similar)
   - Click the blue shark fin icon to start capturing

2. **Set Filter (IMPORTANT):**
   - In the filter box at the top, type:
     ```
     http and tcp.port == 8000
     ```
   - Press Enter
   - This filters for HTTP traffic on port 8000

3. **Verify Backend is Running on HTTP:**
   ```powershell
   cd backend
   USE_HTTP=true python main.py
   ```
   - You should see: `[!] VULNERABLE: Running on HTTP (unencrypted)`
   - Server should be on `http://localhost:8000`

### Step 4: Make a Login Request

**Option A: Using curl (Recommended)**
```powershell
curl -X POST http://localhost:8000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\": \"admin@university.edu\", \"password\": \"admin123\"}'
```

**Option B: Using the demonstration script**
```powershell
cd backend
python demonstrate_network_exposure.py
```

**Option C: Using the frontend**
- Open browser to `http://localhost:3000`
- Try to login (this will go through the Vite proxy)

### Step 5: Find the HTTP Request in Wireshark

1. **Look for HTTP packets:**
   - You should see packets with protocol "HTTP"
   - Look for:
     - `POST /api/v1/auth/login HTTP/1.1`
     - Or `GET /api/v1/courses HTTP/1.1`

2. **If you don't see HTTP packets:**
   - Check the filter: `http and tcp.port == 8000`
   - Try removing the filter temporarily to see all traffic
   - Make sure backend is running on HTTP (not HTTPS)
   - Try a different interface

3. **View the Request:**
   - Find a packet with "POST" in the Info column
   - Right-click on the packet
   - Select: **Follow → HTTP Stream**
   - A new window will open showing the HTTP conversation

4. **In the HTTP Stream window:**
   - You'll see the request (red) and response (blue)
   - Look for the request body containing:
     ```json
     {"email": "admin@university.edu", "password": "admin123"}
     ```
   - The password should be visible in plaintext!

## Alternative: Use RawCap (If Npcap Loopback Doesn't Work)

If the loopback adapter doesn't work, use RawCap:

1. **Download RawCap:**
   - Go to: https://www.netresec.com/?page=RawCap
   - Download RawCap.exe

2. **Capture localhost traffic:**
   ```powershell
   # Run as Administrator
   .\RawCap.exe 127.0.0.1 capture.pcap
   ```

3. **Make your requests** (in another terminal)

4. **Stop RawCap** (Ctrl+C)

5. **Open capture.pcap in Wireshark:**
   - File → Open → select capture.pcap
   - Apply filter: `http and tcp.port == 8000`

## Alternative: Use 0.0.0.0 Instead of localhost

Sometimes it's easier to bind to 0.0.0.0 and capture on your main network interface:

1. **Backend is already configured** to listen on `0.0.0.0:8000`

2. **In Wireshark:**
   - Select your main network interface (Ethernet or Wi-Fi)
   - Filter: `http and (ip.addr == 127.0.0.1 or ip.addr == ::1) and tcp.port == 8000`
   - This might work if your interface captures localhost traffic

## Troubleshooting

### Problem: No packets captured

**Solutions:**
1. Make sure backend is running: `USE_HTTP=true python main.py`
2. Verify server is on HTTP (check console output)
3. Try accessing `http://localhost:8000` in browser first
4. Check if port 8000 is actually being used:
   ```powershell
   netstat -an | findstr :8000
   ```

### Problem: Only see TCP packets, not HTTP

**Solutions:**
1. Make sure you're using HTTP (not HTTPS)
2. Check filter: `http and tcp.port == 8000`
3. Try: `tcp.port == 8000` first to see all traffic
4. Right-click TCP packet → Decode As → HTTP

### Problem: Can't find loopback adapter

**Solutions:**
1. Reinstall Npcap with loopback support
2. Restart Wireshark
3. Run Wireshark as Administrator
4. Use RawCap as alternative

### Problem: Filter shows no results

**Try these filters one by one:**
```
tcp.port == 8000
http
ip.addr == 127.0.0.1
tcp.port == 8000 and ip.addr == 127.0.0.1
```

### Problem: See packets but can't see HTTP content

**Solutions:**
1. Right-click packet → Follow → TCP Stream (then look for HTTP)
2. Check packet details pane (middle section) - expand HTTP section
3. Make sure you're looking at the right packet (POST request)

## Step-by-Step Visual Guide

### 1. Start Backend on HTTP
```powershell
cd D:\UNI\ACS\ACSProject\ACS_Project\backend
USE_HTTP=true python main.py
```
**Expected output:**
```
[!] VULNERABLE: Running on HTTP (unencrypted)
    All data transmitted in plaintext - visible in network traffic
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Open Wireshark (as Administrator)

### 3. Select Interface
- Look for: `Npcap Loopback Adapter` or `Adapter for loopback traffic capture`
- If not available, use your main network interface

### 4. Start Capture
- Click blue shark fin icon
- Filter: `http and tcp.port == 8000`

### 5. Make Request
```powershell
curl -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\": \"admin@university.edu\", \"password\": \"admin123\"}"
```

### 6. Stop Capture
- Click red square icon

### 7. Find HTTP Packet
- Look for packet with "POST /api/v1/auth/login" in Info column
- Right-click → Follow → HTTP Stream

### 8. View Plaintext Data
- In HTTP Stream window, you'll see:
  ```
  POST /api/v1/auth/login HTTP/1.1
  Host: localhost:8000
  Content-Type: application/json
  
  {"email": "admin@university.edu", "password": "admin123"}
  ```

## Verification Checklist

- [ ] Npcap installed with loopback support
- [ ] Wireshark running as Administrator
- [ ] Loopback adapter visible in interface list
- [ ] Backend running on HTTP (`USE_HTTP=true`)
- [ ] Filter set: `http and tcp.port == 8000`
- [ ] Made a request (curl or browser)
- [ ] Found HTTP packet in Wireshark
- [ ] Opened HTTP Stream
- [ ] Can see password in plaintext

## Quick Test Command

Run this to verify everything works:

```powershell
# Terminal 1: Start backend
cd backend
USE_HTTP=true python main.py

# Terminal 2: Make request
curl http://localhost:8000/health

# In Wireshark: You should see GET /health request
```

If you see the GET request, then login requests will work the same way!

## Alternative: Browser DevTools (Easiest Method - No Wireshark Needed!)

**This is the SIMPLEST way to see unencrypted data without Wireshark setup:**

1. **Start backend on HTTP:**
   ```powershell
   cd backend
   USE_HTTP=true python main.py
   ```

2. **Open browser to frontend:**
   - Go to `http://localhost:3000`
   - Open DevTools: Press `F12` or Right-click → Inspect

3. **Go to Network tab:**
   - Click "Network" tab in DevTools
   - Make sure "Preserve log" is checked

4. **Make a login request:**
   - Enter credentials and click Login
   - OR use the frontend to make any API call

5. **View the request:**
   - Find the request to `/api/v1/auth/login` in the Network tab
   - Click on it
   - Go to "Payload" or "Request" tab
   - You'll see the password in the request body!
   - Go to "Response" tab to see the response (may contain sensitive data)

**Advantages:**
- No Wireshark setup needed
- No Npcap installation needed
- Works immediately
- Shows request/response clearly
- Perfect for demonstrating data exposure

**This is sufficient to demonstrate that sensitive data is transmitted without encryption!**

## Still Having Issues with Wireshark?

1. **Use Browser DevTools** (recommended - see above)
2. **Try RawCap** (simpler than Wireshark for localhost):
   - Download: https://www.netresec.com/?page=RawCap
   - Run: `RawCap.exe 127.0.0.1 capture.pcap` (as Admin)
   - Make requests
   - Open capture.pcap in Wireshark
3. **Check Windows Firewall** - might be blocking
4. **Try different port** - test with port 8080 instead
5. **Use main network interface** instead of loopback:
   - Select your Ethernet/Wi-Fi interface
   - Filter: `tcp.port == 8000`
   - May work if interface captures localhost traffic

