# Simple curl-based API endpoint enumeration
# Fetches OpenAPI schema and generates api_endpoints.md

$baseUrl = "http://localhost:8000"
$outputFile = "recon/api_endpoints.md"

Write-Host "Fetching API endpoints from $baseUrl..."
Write-Host ""

# Fetch OpenAPI schema using curl (via PowerShell)
try {
    Write-Host "[*] Fetching OpenAPI schema..."
    $openapiJson = curl.exe -s "$baseUrl/openapi.json" | ConvertFrom-Json
    
    Write-Host "[+] Found $(($openapiJson.paths.PSObject.Properties | Measure-Object).Count) API paths"
    Write-Host ""
    
    # Generate markdown report
    $report = "# API Endpoints Discovery Report`n`n"
    $report += "## Reconnaissance Date`n"
    $report += "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n"
    $report += "## Target`n"
    $report += "- **Base URL**: $baseUrl`n"
    $report += "- **API Title**: $($openapiJson.info.title)`n"
    $report += "- **API Version**: $($openapiJson.info.version)`n"
    $report += "- **Discovery Method**: OpenAPI schema (`/openapi.json`)`n`n"
    
    # Group endpoints by tags
    $endpointsByTag = @{}
    
    foreach ($path in $openapiJson.paths.PSObject.Properties) {
        $pathName = $path.Name
        foreach ($method in $path.Value.PSObject.Properties) {
            $methodName = $method.Name.ToUpper()
            $endpoint = $method.Value
            
            # Get tags (group endpoints by functionality)
            $tags = if ($endpoint.tags) { $endpoint.tags } else { @("Other") }
            
            foreach ($tag in $tags) {
                if (-not $endpointsByTag.ContainsKey($tag)) {
                    $endpointsByTag[$tag] = @()
                }
                
                $endpointsByTag[$tag] += @{
                    Path = $pathName
                    Method = $methodName
                    Summary = $endpoint.summary
                    Description = $endpoint.description
                    Parameters = $endpoint.parameters
                    RequestBody = $endpoint.requestBody
                }
            }
        }
    }
    
    # Write endpoints grouped by tags
    $report += "## API Endpoints`n`n"
    
    foreach ($tag in ($endpointsByTag.Keys | Sort-Object)) {
        $report += "### $tag`n`n"
        $report += "| Path | Method | Summary |`n"
        $report += "|------|--------|---------|`n"
        
        foreach ($endpoint in ($endpointsByTag[$tag] | Sort-Object Path, Method)) {
            $path = $endpoint.Path
            $method = $endpoint.Method
            $summary = if ($endpoint.Summary) { 
                $endpoint.Summary -replace '\|', '\|'  # Escape pipes in markdown
            } else { 
                "-" 
            }
            
            $report += "| $path | $method | $summary |`n"
        }
        
        $report += "`n"
    }
    
    # Add detailed endpoint information
    $report += "## Detailed Endpoint Information`n`n"
    
    foreach ($path in ($openapiJson.paths.PSObject.Properties | Sort-Object Name)) {
        $pathName = $path.Name
        $report += "### $pathName`n`n"
        
        foreach ($method in ($path.Value.PSObject.Properties | Sort-Object Name)) {
            $methodName = $method.Name.ToUpper()
            $endpoint = $method.Value
            
            $report += "**$methodName $pathName**`n`n"
            
            if ($endpoint.summary) {
                $report += "- **Summary**: $($endpoint.summary)`n"
            }
            if ($endpoint.description) {
                $report += "- **Description**: $($endpoint.description)`n"
            }
            
            # Parameters
            if ($endpoint.parameters) {
                $report += "- **Parameters**:`n"
                foreach ($param in $endpoint.parameters) {
                    $paramType = if ($param.schema.type) { $param.schema.type } else { "unknown" }
                    $required = if ($param.required) { "required" } else { "optional" }
                    $report += "  - `$($param.name)` ($paramType, $required)`n"
                }
            }
            
            # Request body
            if ($endpoint.requestBody) {
                $report += "- **Request Body**: Required`n"
            }
            
            # Responses
            if ($endpoint.responses) {
                $report += "- **Responses**:`n"
                foreach ($response in $endpoint.responses.PSObject.Properties) {
                    $statusCode = $response.Name
                    $description = if ($response.Value.description) { $response.Value.description } else { "-" }
                    $report += "  - $statusCode : $description`n"
                }
            }
            
            $report += "`n"
        }
    }
    
    # Summary
    $totalEndpoints = ($openapiJson.paths.PSObject.Properties | ForEach-Object { 
        ($_.Value.PSObject.Properties | Measure-Object).Count 
    } | Measure-Object -Sum).Sum
    
    $report += "## Summary`n`n"
    $report += "- **Total API Paths**: $(($openapiJson.paths.PSObject.Properties | Measure-Object).Count)`n"
    $report += "- **Total Endpoints**: $totalEndpoints`n"
    $report += "- **API Groups**: $(($endpointsByTag.Keys | Measure-Object).Count)`n"
    $report += "`n"
    
    # Notes
    $report += "## Notes`n`n"
    $report += "- Endpoints discovered from OpenAPI schema at `/openapi.json``n"
    $report += "- Interactive documentation available at `/docs` (Swagger UI)`n"
    $report += "- Alternative documentation at `/redoc` (ReDoc)`n"
    $report += "- Server must be running to access endpoints`n"
    
    # Write to file
    $report | Out-File -FilePath $outputFile -Encoding UTF8
    
    Write-Host "[+] Report saved to: $outputFile"
    Write-Host "[+] Total endpoints: $totalEndpoints"
    
} catch {
    Write-Host "[-] Error: $($_.Exception.Message)"
    Write-Host "[-] Make sure the backend server is running at $baseUrl"
    Write-Host "[-] Try: cd backend && python main.py"
    exit 1
}
