# Using Browser DevTools to Demonstrate Data Exposure

**This is the EASIEST method** to demonstrate that sensitive data is transmitted without encryption. No Wireshark setup required!

**Works with both HTTP and HTTPS!** Browser DevTools shows the data before/after encryption, so you can see sensitive data even with HTTPS.

## Why Use Browser DevTools?

- ✅ No installation needed (built into browsers)
- ✅ Works immediately
- ✅ Shows request/response clearly
- ✅ Perfect for demonstrating data exposure
- ✅ No need for Npcap or Wireshark setup

## Step-by-Step Instructions

### 1. Start Backend

**Option A: HTTP (Unencrypted)**
```powershell
cd backend
USE_HTTP=true python main.py
```
**Verify:** You should see `[!] VULNERABLE: Running on HTTP (unencrypted)`

**Option B: HTTPS (Misconfigured Certificate)**
```powershell
cd backend
python main.py  # Runs on HTTPS by default
```
**Verify:** You should see `[!] VULNERABLE: Running on HTTPS with misconfigured certificate`
**Note:** Browser will show certificate warning - click "Advanced" → "Proceed to localhost (unsafe)"

### 2. Open Frontend in Browser

- Navigate to: `http://localhost:3000` (frontend always uses HTTP)
- Make sure frontend is running: `npm run dev` (in frontend directory)
- **Note:** Frontend proxy will forward to backend (HTTP or HTTPS)

### 3. Open Browser DevTools

**Chrome/Edge:**
- Press `F12`
- OR Right-click → Inspect
- OR `Ctrl + Shift + I`

**Firefox:**
- Press `F12`
- OR Right-click → Inspect Element
- OR `Ctrl + Shift + I`

### 4. Go to Network Tab

- Click on "Network" tab in DevTools
- **Important:** Check "Preserve log" checkbox (so requests don't disappear)

### 5. Make a Login Request

**Option A: Use the Login Form**
- Enter email: `admin@university.edu`
- Enter password: `admin123`
- Click "Login" button

**Option B: Use Browser Console**
- Go to "Console" tab
- Run:
  ```javascript
  fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email: 'admin@university.edu', password: 'admin123'})
  })
  ```

### 6. View the Request in Network Tab

1. **Find the request:**
   - Look for `login` or `/api/v1/auth/login` in the Network tab
   - Click on it

2. **View Request Payload:**
   - Click on "Payload" tab (Chrome) or "Request" tab (Firefox)
   - Expand "Request Payload" or "Form Data"
   - **You'll see:**
     ```json
     {
       "email": "admin@university.edu",
       "password": "admin123"
     }
     ```
   - **The password is visible in plaintext!**

3. **View Response:**
   - Click on "Response" or "Preview" tab
   - You'll see the server response
   - May contain sensitive data

### 7. View Other Sensitive Data

**Get All Users (Password Hashes):**
1. In Console tab, run:
   ```javascript
   fetch('http://localhost:8000/api/v1/auth/users')
     .then(r => r.json())
     .then(console.log)
   ```
2. In Network tab, find the request to `/api/v1/auth/users`
3. Click on it → Response tab
4. **You'll see password hashes in the response!**

## Screenshot Example

What you should see in DevTools:

**Request Payload:**
```
email: "admin@university.edu"
password: "admin123"  ← VULNERABLE: Visible in plaintext
```

**Response:**
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

## Demonstrating Password Hash Exposure

1. **In Console tab, run:**
   ```javascript
   fetch('http://localhost:8000/api/v1/auth/users')
     .then(r => r.json())
     .then(data => {
       console.log('Users:', data);
       console.log('Password hash:', data[0].password_hash);
     })
   ```

2. **In Network tab:**
   - Find request to `/api/v1/auth/users`
   - Click on it
   - View Response tab
   - **Password hashes are visible!**

## Advantages Over Wireshark

- ✅ No installation required
- ✅ Works immediately
- ✅ Clear request/response view
- ✅ Easy to screenshot for documentation
- ✅ Shows exactly what's being transmitted
- ✅ Perfect for demonstrating the vulnerability

## What This Demonstrates

1. **Passwords transmitted in plaintext** - visible in request payload
2. **Password hashes exposed** - visible in API responses
3. **Data exposure** - all data visible in DevTools (even with HTTPS, DevTools shows decrypted data)
4. **Real-world impact** - shows what attackers could see

**Note:** With HTTPS, the data is encrypted in transit, but:
- Browser DevTools shows the data before encryption (client-side)
- Misconfigured certificate allows man-in-the-middle attacks
- Browser warnings can be bypassed by users
- Demonstrates the vulnerability of misconfigured certificates

## For Your Security Assessment

This method is **perfectly valid** for demonstrating data exposure:
- Shows data in transit (Network tab)
- Shows lack of encryption (plaintext visible)
- Easy to document (screenshots)
- Demonstrates real-world vulnerability

**You don't need Wireshark** - Browser DevTools is sufficient and easier!

## Additional Tests

### Test 1: Login Request
- Shows password in request payload

### Test 2: Get Users
- Shows password hashes in response

### Test 3: User Registration
- Shows password in request
- Shows password hash in response

### Test 4: Debug Endpoint
```javascript
fetch('http://localhost:8000/api/v1/debug/info')
  .then(r => r.json())
  .then(console.log)
```
- Shows system information, environment variables, database connection strings

All of these demonstrate **sensitive data transmitted without encryption**!

