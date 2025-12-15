# Quick Start: Testing with HTTPS

## Testing Data Exposure with HTTPS (Misconfigured Certificate)

### Method 1: Browser DevTools (Easiest - Works with HTTPS!)

**Browser DevTools shows data before encryption, so it works perfectly with HTTPS!**

1. **Start backend on HTTPS:**
   ```powershell
   cd backend
   python main.py  # Runs on HTTPS by default
   ```

2. **Update frontend proxy (if needed):**
   - Edit `frontend/vite.config.js`
   - Change target to: `'https://localhost:8000'`
   - Add: `secure: false` (to accept misconfigured certificate)
   - Restart frontend: `npm run dev`

3. **Open browser:**
   - Go to `http://localhost:3000`
   - Press `F12` → Network tab

4. **Make login request:**
   - Use login form
   - OR in Console tab:
     ```javascript
     fetch('https://localhost:8000/api/v1/auth/login', {
       method: 'POST',
       headers: {'Content-Type': 'application/json'},
       body: JSON.stringify({email: 'admin@university.edu', password: 'admin123'})
     })
     ```

5. **View request:**
   - Find `/api/v1/auth/login` in Network tab
   - Click on it → Payload tab
   - **Password visible in plaintext!** (even though sent over HTTPS)

### Method 2: Direct Browser Access (See Certificate Warnings)

1. **Start backend:**
   ```powershell
   cd backend
   python main.py
   ```

2. **Open browser to:**
   ```
   https://localhost:8000
   ```

3. **Observe certificate warnings:**
   - Browser will show security warning
   - Click "Advanced" → "Proceed to localhost (unsafe)"
   - **This demonstrates the vulnerability!**

4. **View certificate details:**
   - Click lock/warning icon
   - See: Expired, Wrong CN, Self-signed
   - Take screenshot for documentation

### Method 3: Wireshark with TLS Decryption

1. **Start backend on HTTPS:**
   ```powershell
   cd backend
   python main.py
   ```

2. **Configure Wireshark:**
   - Edit → Preferences → Protocols → TLS
   - RSA keys list → Add
   - IP: `127.0.0.1`, Port: `8000`, Protocol: `http`
   - Key file: `backend/key.pem`

3. **Capture and decrypt:**
   - Filter: `tls and tcp.port == 8000`
   - Make requests
   - Follow → TLS Stream
   - See decrypted data

## What HTTPS Testing Shows

✅ **Certificate Misconfiguration:**
- Expired certificate
- Wrong Common Name
- Self-signed certificate
- Users can bypass warnings

✅ **Data Exposure:**
- Browser DevTools shows plaintext (client-side)
- With private key, traffic can be decrypted
- Demonstrates man-in-the-middle vulnerability

✅ **Real-World Impact:**
- Shows HTTPS alone isn't sufficient
- Misconfigured certificates allow interception
- Users may accept invalid certificates

## See Also

- `HTTPS_TESTING_GUIDE.md` - Detailed HTTPS testing guide
- `BROWSER_DEVTOOLS_GUIDE.md` - Browser DevTools instructions
- `WIRESHARK_LOCALHOST_GUIDE.md` - Wireshark setup

