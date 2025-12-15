# API Endpoint Enumeration Script
# This script enumerates API endpoints using multiple methods:
# 1. OpenAPI schema discovery (FastAPI)
# 2. Common path brute-forcing
# 3. HTTP method testing

$outputFile = "recon/api_endpoints.md"
$baseUrl = "http://localhost:8000"

Write-Host "Enumerating API endpoints at $baseUrl..."
Write-Host ""

# Common wordlist for directory/file enumeration
$commonPaths = @(
    "/api", "/api/v1", "/api/v2", "/api/v3",
    "/admin", "/auth", "/login", "/logout", "/register",
    "/users", "/courses", "/enrollments", "/audit", "/debug",
    "/docs", "/redoc", "/openapi.json", "/swagger.json",
    "/health", "/status", "/ping", "/version",
    "/.env", "/config", "/backup", "/test", "/dev",
    "/api/v1/auth", "/api/v1/courses", "/api/v1/enrollments",
    "/api/v1/admin", "/api/v1/audit", "/api/v1/debug"
)

# HTTP methods to test
$methods = @("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD")

# Results storage
$results = @{
    Endpoints = @()
    OpenAPI = $null
    Discovered = @()
}

# Function to test endpoint
function Test-Endpoint {
    param(
        [string]$Path,
        [string]$Method = "GET"
    )
    
    $url = "$baseUrl$Path"
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method $Method -UseBasicParsing -ErrorAction Stop -TimeoutSec 5
        return @{
            Path = $Path
            Method = $Method
            StatusCode = $response.StatusCode
            ContentType = $response.Headers.'Content-Type'
            ContentLength = $response.RawContentLength
            Headers = $response.Headers
            Success = $true
        }
    } catch {
        $statusCode = if ($_.Exception.Response) { 
            [int]$_.Exception.Response.StatusCode.value__ 
        } else { 
            "Error" 
        }
        return @{
            Path = $Path
            Method = $Method
            StatusCode = $statusCode
            Success = $false
            Error = $_.Exception.Message
        }
    }
}

# 1. Get OpenAPI schema (FastAPI)
Write-Host "[1/3] Fetching OpenAPI schema..."
try {
    $openapiResponse = Invoke-WebRequest -Uri "$baseUrl/openapi.json" -UseBasicParsing -ErrorAction Stop
    $openapiData = $openapiResponse.Content | ConvertFrom-Json
    $results.OpenAPI = $openapiData
    
    Write-Host "  ✓ OpenAPI schema found - $(($openapiData.paths.PSObject.Properties | Measure-Object).Count) paths discovered"
    
    # Extract endpoints from OpenAPI
    foreach ($path in $openapiData.paths.PSObject.Properties) {
        $pathName = $path.Name
        foreach ($method in $path.Value.PSObject.Properties) {
            $methodName = $method.Name.ToUpper()
            $results.Endpoints += @{
                Path = $pathName
                Method = $methodName
                Summary = $method.Value.summary
                Tags = $method.Value.tags -join ", "
                Source = "OpenAPI"
            }
        }
    }
} catch {
    Write-Host "  ✗ OpenAPI schema not accessible: $($_.Exception.Message)"
}

# 2. Test common paths
Write-Host ""
Write-Host "[2/3] Testing common paths..."
$testedPaths = @()
foreach ($path in $commonPaths) {
    if (-not $testedPaths.Contains($path)) {
        $testedPaths += $path
        $result = Test-Endpoint -Path $path -Method "GET"
        if ($result.Success -and $result.StatusCode -lt 500) {
            $results.Discovered += $result
            Write-Host "  ✓ $path - Status: $($result.StatusCode)"
        }
    }
}

# 3. Test HTTP methods on discovered endpoints
Write-Host ""
Write-Host "[3/3] Testing HTTP methods on discovered endpoints..."
$uniquePaths = $results.Discovered | Select-Object -ExpandProperty Path -Unique
foreach ($path in $uniquePaths) {
    foreach ($method in $methods) {
        if ($method -ne "GET") {  # Already tested GET
            $result = Test-Endpoint -Path $path -Method $method
            if ($result.Success -and $result.StatusCode -ne 405) {  # 405 = Method Not Allowed
                $results.Discovered += $result
                Write-Host "  ✓ $method $path - Status: $($result.StatusCode)"
            }
        }
    }
}

# Generate markdown report
Write-Host ""
Write-Host "Generating report..."

$report = "# API Endpoints Discovery Report`n`n"
$report += "## Reconnaissance Date`n"
$report += "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n"
$report += "## Target`n"
$report += "- **Base URL**: $baseUrl`n"
$report += "- **Discovery Method**: OpenAPI schema + Path enumeration + HTTP method testing`n`n"

# OpenAPI endpoints
if ($results.OpenAPI) {
    $report += "## Endpoints from OpenAPI Schema`n`n"
    $report += "| Path | Method | Summary | Tags |`n"
    $report += "|------|--------|---------|------|`n"
    
    $uniqueEndpoints = $results.Endpoints | Sort-Object Path, Method | Select-Object -Unique
    foreach ($endpoint in $uniqueEndpoints) {
        $path = $endpoint.Path
        $method = $endpoint.Method
        $summary = if ($endpoint.Summary) { $endpoint.Summary } else { "-" }
        $tags = if ($endpoint.Tags) { $endpoint.Tags } else { "-" }
        $report += "| $path | $method | $summary | $tags |`n"
    }
    $report += "`n"
}

# Discovered endpoints
if ($results.Discovered.Count -gt 0) {
    $report += "## Discovered Endpoints (Brute Force)`n`n"
    $report += "| Path | Method | Status Code | Content-Type | Notes |`n"
    $report += "|------|--------|-------------|--------------|-------|`n"
    
    $uniqueDiscovered = $results.Discovered | Sort-Object Path, Method | Select-Object -Unique
    foreach ($endpoint in $uniqueDiscovered) {
        $path = $endpoint.Path
        $method = $endpoint.Method
        $status = $endpoint.StatusCode
        $contentType = if ($endpoint.ContentType) { $endpoint.ContentType } else { "-" }
        $notes = if ($status -eq 200) { "Active endpoint" } 
                 elseif ($status -eq 401) { "Requires authentication" }
                 elseif ($status -eq 403) { "Forbidden" }
                 elseif ($status -eq 404) { "Not found" }
                 elseif ($status -eq 405) { "Method not allowed" }
                 else { "Status: $status" }
        $report += "| $path | $method | $status | $contentType | $notes |`n"
    }
    $report += "`n"
}

# Summary
$report += "## Summary`n`n"
$report += "- **Total endpoints discovered**: $(($results.Endpoints | Measure-Object).Count + ($results.Discovered | Measure-Object).Count)`n"
$report += "- **From OpenAPI**: $(($results.Endpoints | Measure-Object).Count)`n"
$report += "- **From enumeration**: $(($results.Discovered | Measure-Object).Count)`n"
$report += "`n"

# API Structure
$report += "## API Structure`n`n"
$report += "### Base Paths`n"
$report += "- `/api/v1/auth` - Authentication endpoints`n"
$report += "- `/api/v1/courses` - Course management`n"
$report += "- `/api/v1/enrollments` - Enrollment management`n"
$report += "- `/api/v1/admin` - Administrative functions`n"
$report += "- `/api/v1/audit` - Audit logging`n"
$report += "- `/api/v1/debug` - Debug endpoints (vulnerable)`n"
$report += "`n"

# Documentation endpoints
$report += "### Documentation Endpoints`n"
$report += "- `/docs` - Swagger UI`n"
$report += "- `/redoc` - ReDoc documentation`n"
$report += "- `/openapi.json` - OpenAPI schema`n"
$report += "`n"

# Notes
$report += "## Notes`n`n"
$report += "- This enumeration was performed using PowerShell and OpenAPI schema discovery`n"
$report += "- For more comprehensive enumeration, use tools like `gobuster` or `dirb` (see installation instructions)`n"
$report += "- Some endpoints may require authentication`n"
$report += "- Server must be running during enumeration`n"

# Write to file
$report | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host ""
Write-Host "Report saved to: $outputFile"
Write-Host "Total endpoints discovered: $(($results.Endpoints | Measure-Object).Count + ($results.Discovered | Measure-Object).Count)"
