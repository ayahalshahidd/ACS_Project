# Web Technology Stack Inventory

## Reconnaissance Date
Generated: 2025-12-15 22:36:40

## Methodology
- Manual code inspection
- HTTP header analysis
- Response fingerprinting
- Dependency analysis

---

## Backend Technology Stack

### Web Framework
- **Framework**: FastAPI (Python)
- **Version**: 0.104.1 (from requirements.txt)
- **ASGI Server**: Uvicorn
- **Version**: 0.24.0
- **Detection**: HTTP headers, response format, `/docs` endpoint

### Programming Language
- **Language**: Python 3.10+
- **Platform**: Windows/Linux compatible
- **Event Loop**: asyncio (WindowsSelectorEventLoopPolicy on Windows)

### Database
- **ORM**: SQLAlchemy 2.0.23
- **Database Type**: SQLite (development) / PostgreSQL (production ready)
- **Driver**: psycopg2-binary 2.9.9 (PostgreSQL)

### Authentication & Security
- **JWT Library**: python-jose[cryptography] 3.3.0
- **Password Hashing**: passlib[bcrypt] 1.7.4
- **Cryptography**: cryptography >= 41.0.0
- **Vulnerability**: MD5 hashing used (weak)

### API Features
- **API Documentation**: Swagger UI (FastAPI default)
- **Alternative Docs**: ReDoc
- **CORS**: Enabled (permissive - allows all origins)
- **Content Types**: JSON, form-urlencoded

### SSL/TLS
- **Certificate**: Self-signed, misconfigured
- **Issues**: Expired, wrong CN, self-signed
- **Key Size**: 2048-bit RSA
- **Signature Algorithm**: SHA256

---

## Frontend Technology Stack

### Framework
- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0.8
- **Language**: TypeScript 5.3.3

### HTTP Client
- **Library**: Axios 1.6.2
- **State Management**: @tanstack/react-query 5.12.2

### Routing
- **Library**: react-router-dom 6.20.0

### Development Server
- **Server**: Vite Dev Server
- **Port**: 3000
- **Proxy**: Configured for backend API

---

## Server Headers (Expected)

### HTTP Response Headers
```
Server: uvicorn
Content-Type: application/json
Access-Control-Allow-Origin: http://localhost:3000, http://127.0.0.1:3000
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
```

### API Endpoints
- Base URL: `http://localhost:8000` or `https://localhost:8000`
- API Prefix: `/api/v1`
- Documentation: `/docs` (Swagger), `/redoc` (ReDoc)

---

## Automated Probing Commands

### Using curl (Linux/Mac/Git Bash)
```bash
# Get server headers
curl -I http://localhost:8000

# Get full response headers
curl -v http://localhost:8000

# Probe API endpoints
curl -X GET http://localhost:8000/api/v1/courses
curl -X GET http://localhost:8000/docs

# Check for common files
curl -I http://localhost:8000/robots.txt
curl -I http://localhost:8000/.env
```

### Using PowerShell (Windows)
```powershell
# Get server headers
Invoke-WebRequest -Uri http://localhost:8000 -Method Head -UseBasicParsing

# Get full response
$response = Invoke-WebRequest -Uri http://localhost:8000 -UseBasicParsing
$response.Headers
$response.StatusCode

# Probe API
Invoke-WebRequest -Uri http://localhost:8000/api/v1/courses -UseBasicParsing
Invoke-WebRequest -Uri http://localhost:8000/docs -UseBasicParsing
```

### Using whatweb (if installed)
```bash
# Install whatweb (Ruby gem)
gem install whatweb

# Probe the server
whatweb http://localhost:8000
whatweb -a 3 http://localhost:8000  # Aggressive scan
```

### Using Python requests
```python
import requests

# Get headers
response = requests.get('http://localhost:8000')
print(response.headers)
print(response.status_code)

# Check server info
print(response.headers.get('Server'))
print(response.headers.get('X-Powered-By'))
```

---

## Technology Fingerprints

### FastAPI Indicators
- `/docs` endpoint (Swagger UI)
- `/redoc` endpoint (ReDoc)
- `/openapi.json` endpoint (OpenAPI schema)
- JSON responses with Pydantic validation
- Async/await support

### Uvicorn Indicators
- Server header: "uvicorn"
- ASGI protocol support
- WebSocket support (if enabled)

### React/Vite Indicators
- Frontend served from port 3000
- Hot module replacement (HMR)
- Vite-specific headers in dev mode

---

## Security Headers Analysis

### Missing Security Headers
- No `X-Content-Type-Options`
- No `X-Frame-Options`
- No `Content-Security-Policy`
- No `Strict-Transport-Security` (HSTS)
- No `X-XSS-Protection`

### Present Headers
- `Access-Control-Allow-Origin`: Permissive (vulnerable)
- `Access-Control-Allow-Credentials`: true
- `Access-Control-Allow-Methods`: * (vulnerable)

---

## Version Information

### Backend Dependencies
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose[cryptography]==3.3.0
cryptography>=41.0.0
```

### Frontend Dependencies
```
react@^18.2.0
react-dom@^18.2.0
vite@^5.0.8
typescript@^5.3.3
axios@^1.6.2
```

---

## Network Configuration

### Ports
- Backend HTTP: 8000
- Backend HTTPS: 8000 (with SSL)
- Frontend Dev Server: 3000

### Protocols
- HTTP/1.1
- HTTPS (TLS 1.3)
- WebSocket (if enabled)

---

## File Structure Indicators

### Backend Structure
```
backend/
├── main.py              # FastAPI application
├── database.py          # SQLAlchemy setup
├── models/              # Database models
├── routes/              # API routes
└── requirements.txt     # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/
│   ├── App.tsx          # React app
│   ├── services/
│   │   └── api.ts       # Axios client
│   └── pages/           # React pages
├── package.json         # Node dependencies
└── vite.config.js       # Vite configuration
```

---

## Automated Probing Results

*Run the commands above when the server is running to populate this section*

### HTTP Headers
```
[To be populated by curl/Invoke-WebRequest]
```

### whatweb Results
```
[To be populated by whatweb scan]
```

### Response Analysis
```
[To be populated by probing]
```

---

## Notes

- Server must be running for automated probing
- Use `USE_HTTP=true python main.py` for HTTP mode
- Use `python main.py` for HTTPS mode (with misconfigured certificate)
- Frontend runs on `npm run dev` (port 3000)
