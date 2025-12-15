# Web Technology Stack Inventory - Reconnaissance Results

## Reconnaissance Date
Generated: 2025-12-15 22:56:30

---

## curl Probe Results

### HTTP Headers (curl -I)
```
HTTP/1.1 200 OK
date: Mon, 15 Dec 2025 20:56:30 GMT
server: uvicorn
content-length: 81
content-type: application/json
```

### Verbose Output (curl -v)
```
* Host localhost:8000 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
* Connected to localhost (127.0.0.1) port 8000
* using HTTP/1.x
> GET / HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/8.13.0
> Accept: */*

< HTTP/1.1 200 OK
< date: Mon, 15 Dec 2025 20:56:30 GMT
< server: uvicorn
< content-length: 81
< content-type: application/json

{"message":"Course Registration System API","version":"1.0.0","status":"running"}
```

### Root Endpoint Response (curl -s)
```
{"message":"Course Registration System API","version":"1.0.0","status":"running"}
```

### /docs Endpoint Probe
```
<title>Course Registration System API - Swagger UI</title>
FastAPI detected via Swagger UI endpoint
```

### /openapi.json Probe
```json
{
  "info": {
    "title": "Course Registration System API",
    "description": "Vulnerable course registration system for security assessment",
    "version": "1.0.0"
  }
}
```

### /health Endpoint
```
{"status":"healthy"}
```

### /api/v1/courses Endpoint
```
Status: 200 OK
Content-Type: application/json
```

---

## Technology Detection

### Detected Technologies
- **Server**: uvicorn
- **Framework**: FastAPI (detected via /docs, /redoc, /openapi.json endpoints)
- **API Documentation**: Swagger UI, ReDoc
- **Content-Type**: application/json
- **Protocol**: HTTP/1.1

### Key Indicators
- Server header: `uvicorn`
- Swagger UI endpoint: `/docs`
- ReDoc endpoint: `/redoc`
- OpenAPI schema: `/openapi.json`
- API prefix: `/api/v1`

---

## whatweb Results

```
whatweb is not installed on this system.
To install: gem install whatweb
Then run: whatweb http://localhost:8000
```

---

## Summary

**Web Server**: uvicorn
**Framework**: FastAPI (Python)
**API Version**: 1.0.0
**Base URL**: http://localhost:8000
**Documentation**: Available at /docs and /redoc

