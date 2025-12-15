# API Enumeration: Attacker's Perspective

## Realistic Attacker Workflow

As an attacker, you typically **don't start with gobuster/dirb**. Here's the realistic approach:

---

## Step 1: Check for Documentation (Easiest Win)

**Most APIs expose documentation - attackers check this FIRST:**

```powershell
# Check for Swagger/OpenAPI documentation
curl http://localhost:8000/docs
curl http://localhost:8000/redoc
curl http://localhost:8000/openapi.json

# Or just open in browser
Start-Process http://localhost:8000/docs
```

**Why this works:**
- FastAPI exposes `/docs` by default (Swagger UI)
- Shows ALL endpoints, methods, parameters
- No brute-forcing needed - it's all there!

**This is what 90% of attackers do first** - check for documentation endpoints.

---

## Step 2: Use Browser DevTools / Burp Suite

**Intercept traffic while using the application:**

1. **Browser DevTools** (Network tab)
   - Use the application normally
   - Watch Network tab for API calls
   - See all endpoints being used

2. **Burp Suite** (Most common attacker tool)
   - Configure browser proxy
   - Browse the application
   - Burp captures all requests
   - Use **Burp Spider** to crawl
   - Use **Burp Intruder** for brute-forcing (if needed)

---

## Step 3: Manual Testing with curl/PowerShell

**Test common endpoints manually:**

```powershell
# Test root endpoint
curl http://localhost:8000/

# Test common API paths
curl http://localhost:8000/api/v1/courses
curl http://localhost:8000/api/v1/auth/login

# Test different HTTP methods
curl -X OPTIONS http://localhost:8000/api/v1/auth
curl -X HEAD http://localhost:8000/api/v1/courses
```

---

## Step 4: Only Then Use gobuster/dirb (If Needed)

**Use brute-forcing tools ONLY when:**
- No documentation available
- Looking for hidden/undocumented endpoints
- Comprehensive security assessment

**Most attackers skip this** if they already found documentation.

---

## Realistic Attacker Script

Here's what an attacker would actually run:

```powershell
# 1. Check for documentation (FASTEST)
Write-Host "[*] Checking for API documentation..."
try {
    $docs = Invoke-WebRequest -Uri "http://localhost:8000/docs" -UseBasicParsing
    Write-Host "[+] Found Swagger UI at /docs"
    Write-Host "[+] All endpoints visible - no brute-forcing needed!"
} catch {
    Write-Host "[-] No Swagger UI found"
}

# 2. Get OpenAPI schema (contains all endpoints)
try {
    $openapi = Invoke-WebRequest -Uri "http://localhost:8000/openapi.json" -UseBasicParsing
    $schema = $openapi.Content | ConvertFrom-Json
    Write-Host "[+] OpenAPI schema found - $(($schema.paths.PSObject.Properties | Measure-Object).Count) endpoints"
    
    # Extract all endpoints
    foreach ($path in $schema.paths.PSObject.Properties) {
        Write-Host "  Found: $($path.Name)"
    }
} catch {
    Write-Host "[-] OpenAPI schema not accessible"
}

# 3. Test a few common endpoints manually
Write-Host "`n[*] Testing common endpoints..."
$endpoints = @("/", "/health", "/api/v1/courses", "/api/v1/auth/login")
foreach ($ep in $endpoints) {
    try {
        $r = Invoke-WebRequest -Uri "http://localhost:8000$ep" -UseBasicParsing -ErrorAction Stop
        Write-Host "[+] $ep - Status: $($r.StatusCode)"
    } catch {
        $status = if ($_.Exception.Response) { $_.Exception.Response.StatusCode.value__ } else { "Error" }
        Write-Host "[-] $ep - Status: $status"
    }
}
```

---

## Why This Approach?

1. **Documentation is fastest** - Why brute-force when docs show everything?
2. **Burp Suite is standard** - Most attackers use it, not gobuster
3. **Manual testing is effective** - Test what you see, not random paths
4. **gobuster/dirb are last resort** - Only for hidden endpoints

---

## For Your Project

Since this is FastAPI with `/docs` endpoint:

**As an attacker, you would:**
1. ✅ Visit `http://localhost:8000/docs` (finds everything instantly)
2. ✅ Use Burp Suite to intercept while testing
3. ✅ Maybe test a few common paths manually
4. ❌ **Skip gobuster/dirb** - not needed when docs are available

---

## Summary

**Do you need gobuster/dirb?**
- **No** - if documentation is available (like FastAPI `/docs`)
- **Yes** - if you're looking for hidden/undocumented endpoints
- **Maybe** - for comprehensive security assessment

**Most realistic attacker approach:**
1. Check `/docs` or `/swagger` first
2. Use Burp Suite for interception
3. Manual testing with curl/browser
4. gobuster/dirb only if needed

The PowerShell script I created already does the realistic approach - it checks OpenAPI first, then tests common paths. You don't need gobuster/dirb for this project!
