# Launch Options: HTTP vs HTTPS

This guide explains how to run both the frontend and backend on HTTP or HTTPS based on launch options.

## Quick Start

### Option 1: Run Everything on HTTP (Unencrypted)

**Terminal 1 - Backend:**
```powershell
cd backend
USE_HTTP=true python main.py
```

**Terminal 2 - Frontend (IMPORTANT: Must be in frontend directory!):**
```powershell
cd frontend
npm run dev:http
# OR
USE_HTTP=true npm run dev
```

**Note:** Make sure you're in the `frontend` directory when running npm commands!

**Result:**
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000` (proxies to HTTP backend)
- All traffic unencrypted - perfect for Wireshark analysis

### Option 2: Run Everything on HTTPS (Misconfigured Certificate)

**Terminal 1 - Backend:**
```powershell
cd backend
python main.py  # HTTPS by default
```

**Terminal 2 - Frontend (IMPORTANT: Must be in frontend directory!):**
```powershell
cd frontend
npm run dev:https
# OR
USE_HTTP=false npm run dev
```

**Note:** Make sure you're in the `frontend` directory when running npm commands!

**Result:**
- Backend: `https://localhost:8000` (misconfigured certificate)
- Frontend: `http://localhost:3000` (proxies to HTTPS backend)
- Browser will show certificate warnings

## Environment Variables

### Backend Protocol Control

The backend uses the `USE_HTTP` environment variable:

- `USE_HTTP=true` or `USE_HTTP=1` → Backend runs on HTTP
- `USE_HTTP=false` or `USE_HTTP=0` or unset → Backend runs on HTTPS

**Command line flag alternative:**
```powershell
python main.py --http  # Forces HTTP mode
```

### Frontend Proxy Configuration

The frontend automatically detects the backend protocol from `USE_HTTP`:

- `USE_HTTP=true` → Frontend proxy points to `http://localhost:8000`
- `USE_HTTP=false` or unset → Frontend proxy points to `https://localhost:8000`

**Manual override:**
```powershell
VITE_API_URL=https://localhost:8000 npm run dev  # Force HTTPS backend
VITE_API_URL=http://localhost:8000 npm run dev  # Force HTTP backend
```

## NPM Scripts

The frontend includes convenient npm scripts:

```json
"dev"         → Uses default (HTTPS if USE_HTTP not set)
"dev:http"    → Forces HTTP backend
"dev:https"   → Forces HTTPS backend
```

## Examples

### Example 1: HTTP Mode (Network Analysis)

**Terminal 1 - Backend:**
```powershell
cd backend
USE_HTTP=true python main.py
```

**Terminal 2 - Frontend (IMPORTANT: cd to frontend first!):**
```powershell
cd frontend
npm run dev:http
```

**Access:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- All traffic unencrypted - visible in Wireshark

### Example 2: HTTPS Mode (Certificate Testing)

**Terminal 1 - Backend:**
```powershell
cd backend
python main.py  # HTTPS by default
```

**Terminal 2 - Frontend (IMPORTANT: cd to frontend first!):**
```powershell
cd frontend
npm run dev:https
```

**Access:**
- Frontend: `http://localhost:3000`
- Backend API: `https://localhost:8000`
- Browser will show certificate warnings
- Frontend proxy accepts misconfigured certificate

### Example 3: Mixed Mode (Not Recommended)

You can run backend on HTTPS and frontend proxy on HTTP (or vice versa), but this may cause issues:

```powershell
# Terminal 1 - Backend on HTTPS
cd backend
python main.py

# Terminal 2 - Frontend proxy to HTTP (will fail - backend is HTTPS!)
cd frontend  # IMPORTANT: Must be in frontend directory!
USE_HTTP=true npm run dev
```

**Recommendation:** Always match frontend and backend protocols.

## How It Works

### Backend (`backend/main.py`)

```python
use_http = os.getenv("USE_HTTP", "false").lower() == "true" or "--http" in sys.argv

if use_http:
    # Run on HTTP
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
else:
    # Run on HTTPS with misconfigured certificate
    uvicorn.run("main:app", host="0.0.0.0", port=8000, 
                ssl_keyfile=key_path, ssl_certfile=cert_path, reload=True)
```

### Frontend (`frontend/vite.config.js`)

```javascript
const useHttp = process.env.USE_HTTP === 'true' || process.env.USE_HTTP === '1'
const backendProtocol = useHttp ? 'http' : 'https'
const backendUrl = process.env.VITE_API_URL || `${backendProtocol}://localhost:8000`

proxy: {
  '/api': {
    target: backendUrl,
    secure: !useHttp ? false : undefined  // Accept invalid certs for HTTPS
  }
}
```

## Testing Scenarios

### Scenario 1: Data Exposure with HTTP

**Goal:** Demonstrate unencrypted data transmission

**Setup:**
```powershell
# Terminal 1 - Backend
cd backend
USE_HTTP=true python main.py

# Terminal 2 - Frontend (IMPORTANT: cd to frontend first!)
cd frontend
npm run dev:http
```

**Test:**
- Open `http://localhost:3000`
- Open DevTools → Network tab
- Make login request
- See password in plaintext in request payload

### Scenario 2: Certificate Misconfiguration with HTTPS

**Goal:** Demonstrate misconfigured certificate vulnerabilities

**Setup:**
```powershell
# Terminal 1 - Backend
cd backend
python main.py  # HTTPS

# Terminal 2 - Frontend (IMPORTANT: cd to frontend first!)
cd frontend
npm run dev:https
```

**Test:**
- Open `http://localhost:3000`
- Browser will show certificate warnings (if accessing backend directly)
- Frontend proxy accepts misconfigured certificate automatically
- Use DevTools to see data (client-side view)

### Scenario 3: Wireshark Analysis

**Goal:** Capture network traffic

**Setup:**
```powershell
# Terminal 1 - Backend
cd backend
USE_HTTP=true python main.py  # HTTP for easier capture

# Terminal 2 - Frontend (IMPORTANT: cd to frontend first!)
cd frontend
npm run dev:http
```

**Test:**
- Start Wireshark
- Filter: `http and tcp.port == 8000`
- Make requests from frontend
- See unencrypted traffic in Wireshark

## Troubleshooting

### Frontend Can't Connect to Backend

**Problem:** Frontend proxy can't reach backend

**Solutions:**
1. **Check backend is running:**
   ```powershell
   # Test backend directly
   curl http://localhost:8000/health  # HTTP
   curl -k https://localhost:8000/health  # HTTPS
   ```

2. **Check protocol mismatch:**
   - If backend is HTTPS, frontend must use `npm run dev:https` or `USE_HTTP=false`
   - If backend is HTTP, frontend must use `npm run dev:http` or `USE_HTTP=true`

3. **Check VITE_API_URL:**
   ```powershell
   # Override if needed
   VITE_API_URL=http://localhost:8000 npm run dev
   ```

### Certificate Warnings in Browser

**Problem:** Browser shows certificate errors

**Solution:** This is expected! The certificate is intentionally misconfigured:
- Expired certificate
- Wrong Common Name
- Self-signed

**To proceed:**
- Click "Advanced" → "Proceed to localhost (unsafe)"
- This demonstrates the vulnerability

### Frontend Shows "Proxy Error"

**Problem:** Vite proxy fails to connect

**Solutions:**
1. **Backend not running:** Start backend first
2. **Wrong protocol:** Match frontend and backend protocols
3. **Port conflict:** Check if port 8000 is in use
4. **Certificate issue (HTTPS):** Frontend should auto-accept with `secure: false`

## Summary

| Backend Mode | Frontend Command | Backend URL | Frontend Proxy |
|-------------|------------------|-------------|----------------|
| HTTP | `npm run dev:http` | `http://localhost:8000` | HTTP |
| HTTPS | `npm run dev:https` | `https://localhost:8000` | HTTPS (accepts invalid cert) |
| HTTP | `USE_HTTP=true npm run dev` | `http://localhost:8000` | HTTP |
| HTTPS | `USE_HTTP=false npm run dev` | `https://localhost:8000` | HTTPS |

**Key Points:**
- Use `USE_HTTP=true` for HTTP mode (both frontend and backend)
- Use `USE_HTTP=false` or unset for HTTPS mode (both frontend and backend)
- Frontend automatically matches backend protocol
- NPM scripts provide convenient shortcuts


