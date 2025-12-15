# API Endpoint Enumeration Guide

This guide explains how to enumerate API endpoints using various tools and methods.

## Quick Start (PowerShell Script)

The easiest way to enumerate endpoints is using the provided PowerShell script:

```powershell
# Make sure backend server is running first!
cd D:\UNI\ACS\ACSProject\ACS_Project
powershell -ExecutionPolicy Bypass -File recon/enumerate_endpoints.ps1
```

This will:
1. Fetch the OpenAPI schema from `/openapi.json`
2. Test common API paths
3. Test different HTTP methods
4. Generate `recon/api_endpoints.md` with results

---

## Method 1: Using gobuster (Recommended)

### Installation (Windows)

**Option A: Using Chocolatey**
```powershell
# Install Chocolatey first if not installed
# Then install gobuster
choco install gobuster
```

**Option B: Manual Installation**
1. Download from: https://github.com/OJ/gobuster/releases
2. Download `gobuster_windows_amd64.exe`
3. Rename to `gobuster.exe`
4. Add to PATH or place in a directory in your PATH

**Option C: Using Go (if you have Go installed)**
```powershell
go install github.com/OJ/gobuster/v3@latest
```

### Usage

```powershell
# Basic directory enumeration
gobuster dir -u http://localhost:8000 -w wordlist.txt

# API-specific enumeration
gobuster dir -u http://localhost:8000/api/v1 -w wordlist.txt -x json,txt

# With extensions and status codes
gobuster dir -u http://localhost:8000 -w wordlist.txt -x json,html -s 200,204,301,302,307,401,403

# Save results to file
gobuster dir -u http://localhost:8000 -w wordlist.txt -o recon/gobuster_results.txt
```

### Recommended Wordlist

Create `recon/api_wordlist.txt`:
```
api
v1
v2
auth
login
logout
register
users
courses
enrollments
admin
audit
debug
docs
redoc
openapi
swagger
health
status
ping
```

Or use common wordlists:
- **SecLists**: https://github.com/danielmiessler/SecLists
- **Common API paths**: `/usr/share/wordlists/dirb/common.txt` (Linux) or download from SecLists

---

## Method 2: Using dirb

### Installation (Windows)

**Option A: Using WSL (Windows Subsystem for Linux)**
```bash
# In WSL
sudo apt-get update
sudo apt-get install dirb
```

**Option B: Manual Installation**
1. Download from: http://dirb.sourceforge.net/
2. Extract and add to PATH
3. Note: dirb is primarily a Linux tool, WSL is recommended

### Usage

```bash
# Basic scan
dirb http://localhost:8000

# With custom wordlist
dirb http://localhost:8000 /path/to/wordlist.txt

# API-specific scan
dirb http://localhost:8000/api/v1 /path/to/wordlist.txt

# Save results
dirb http://localhost:8000 -o recon/dirb_results.txt
```

---

## Method 3: Using OpenAPI Schema (FastAPI)

FastAPI automatically generates an OpenAPI schema. You can use it directly:

```powershell
# Fetch OpenAPI schema
Invoke-WebRequest -Uri http://localhost:8000/openapi.json -OutFile recon/openapi.json

# View in browser
Start-Process http://localhost:8000/docs
```

The OpenAPI schema contains all defined endpoints with their methods, parameters, and responses.

---

## Method 4: Manual Enumeration with curl/PowerShell

### Using curl

```bash
# Test common paths
curl -I http://localhost:8000/api/v1/auth/login
curl -I http://localhost:8000/api/v1/courses
curl -I http://localhost:8000/api/v1/enrollments

# Test different methods
curl -X OPTIONS http://localhost:8000/api/v1/auth
curl -X HEAD http://localhost:8000/api/v1/courses
```

### Using PowerShell

```powershell
# Test endpoint
Invoke-WebRequest -Uri http://localhost:8000/api/v1/courses -Method GET -UseBasicParsing

# Test all HTTP methods
$methods = @("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD")
foreach ($method in $methods) {
    try {
        $response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/courses -Method $method -UseBasicParsing
        Write-Host "$method : $($response.StatusCode)"
    } catch {
        Write-Host "$method : $($_.Exception.Response.StatusCode.value__)"
    }
}
```

---

## Method 5: Using Burp Suite

1. Configure browser to use Burp Suite proxy
2. Navigate through the application
3. Use **Burp Spider** to crawl the site
4. Use **Burp Intruder** to brute-force paths
5. Export results from **Target** tab

---

## Expected Endpoints (From Code Analysis)

Based on the codebase, these endpoints should exist:

### Authentication (`/api/v1/auth`)
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `POST /api/v1/auth/token`
- `POST /api/v1/auth/reset-password`

### Courses (`/api/v1/courses`)
- `GET /api/v1/courses`
- `GET /api/v1/courses/{course_id}`

### Enrollments (`/api/v1/enrollments`)
- `POST /api/v1/enrollments`
- `GET /api/v1/enrollments`
- `DELETE /api/v1/enrollments/{enrollment_id}`

### Admin (`/api/v1/admin`)
- `POST /api/v1/admin/courses`
- `GET /api/v1/admin/courses/{course_id}`
- `POST /api/v1/admin/enrollments/override`

### Audit (`/api/v1/audit`)
- `GET /api/v1/audit`

### Debug (`/api/v1/debug`)
- `GET /api/v1/debug/info`
- `GET /api/v1/debug/users/export`

### Documentation
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc
- `GET /openapi.json` - OpenAPI schema

### System
- `GET /` - Root endpoint
- `GET /health` - Health check

---

## Generating the Report

After enumeration, the results should be saved to `recon/api_endpoints.md` with:

1. **Endpoints from OpenAPI** - All documented endpoints
2. **Discovered endpoints** - Found through enumeration
3. **HTTP methods** - Which methods are allowed
4. **Status codes** - Response codes for each endpoint
5. **Notes** - Authentication requirements, vulnerabilities, etc.

---

## Tips

1. **Always run enumeration with the server running**
2. **Use multiple tools** - Different tools may find different endpoints
3. **Check for hidden endpoints** - Look for:
   - Backup files (`.bak`, `.old`)
   - Version control (`.git`, `.svn`)
   - Configuration files (`.env`, `config.json`)
   - Test endpoints (`/test`, `/dev`, `/staging`)
4. **Test different HTTP methods** - Not all endpoints accept GET
5. **Check for API versioning** - `/api/v1`, `/api/v2`, etc.
6. **Look for documentation** - `/docs`, `/swagger`, `/api-docs`

---

## Troubleshooting

**gobuster not found**
- Make sure it's installed and in your PATH
- Try using the full path: `C:\path\to\gobuster.exe dir ...`

**dirb not found**
- Install via WSL or use gobuster instead
- dirb is primarily a Linux tool

**No endpoints discovered**
- Make sure the backend server is running
- Check the base URL (should be `http://localhost:8000`)
- Try accessing `/docs` in a browser to verify server is up

**Too many 404 errors**
- This is normal - enumeration tests many paths
- Focus on 200, 301, 302, 401, 403 status codes
