# Backend - Course Registration System

Monolithic FastAPI backend with intentional security vulnerabilities.

## Setup

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Generate misconfigured certificate (for HTTPS):**
```bash
python generate_misconfigured_cert.py
```

5. **Run the application:**
```bash
# Run on HTTPS with misconfigured certificate (default)
python main.py

# OR run on HTTP (unencrypted) for network analysis
USE_HTTP=true python main.py
# or
python main.py --http
```

**Note:** The frontend will automatically match the backend protocol. See `LAUNCH_OPTIONS.md` in the project root for details.

The API will be available at:
- **HTTPS (default):** `https://localhost:8000` (VULNERABLE: Misconfigured certificate)
  - Demonstrates certificate misconfiguration vulnerabilities
  - Browser will show certificate warnings
  - See `HTTPS_TESTING_GUIDE.md` for testing with HTTPS
- **HTTP (for testing):** `http://localhost:8000` (VULNERABLE: Unencrypted, use for Wireshark analysis)
  - Easiest for network traffic analysis
  - All data transmitted in plaintext

## API Documentation

Once running, visit:
- Swagger UI: `https://localhost:8000/docs` (HTTPS) or `http://localhost:8000/docs` (HTTP)
- ReDoc: `https://localhost:8000/redoc` (HTTPS) or `http://localhost:8000/redoc` (HTTP)

**Note:** When accessing HTTPS endpoints, browsers will show certificate warnings due to the misconfigured certificate. This is expected behavior for security testing.

## Project Structure

```
backend/
├── main.py              # Main application entry point
├── database.py          # Database configuration
├── requirements.txt     # Python dependencies
├── models/              # SQLAlchemy models
│   ├── user.py
│   ├── course.py
│   ├── enrollment.py
│   └── audit.py
└── routes/              # API routes
    ├── auth.py          # Authentication (VULNERABLE: Broken Auth)
    ├── courses.py       # Courses (VULNERABLE: SQL Injection)
    ├── enrollments.py   # Enrollments (VULNERABLE: CSRF)
    ├── admin.py         # Admin operations
    └── audit.py         # Audit logs (VULNERABLE: Access Control)
```

## Security Vulnerabilities

⚠️ **This application contains intentional vulnerabilities:**

### Server Security
1. **Misconfigured HTTPS Certificates** - Certificate has multiple misconfigurations:
   - Expired certificate (validity expired 6 months ago)
   - Wrong Common Name (CN: `wrong-domain.example.com` instead of `localhost`)
   - Self-signed certificate with mismatched issuer
   - Note: OpenSSL requires minimum 2048-bit keys (weak key size vulnerability cannot be demonstrated due to system restrictions)
   - Note: Modern cryptography libraries require SHA256 signature (weak algorithms like SHA1/MD5 are no longer supported)

2. **Weak Password Storage/Hashing** - Passwords are hashed using MD5:
   - MD5 is cryptographically broken and vulnerable to collision attacks
   - No salt is used, making rainbow table attacks trivial
   - Fast hashing algorithm allows for brute-force attacks
   - Located in `routes/auth.py` - `hash_password()` function

### Application Security
3. **SQL Injection** - `/api/v1/courses?filter=` parameter
4. **Broken Authentication** - No rate limiting, predictable session IDs
5. **CSRF** - `/api/v1/enrollments` lacks CSRF token validation
6. **Access Control** - Audit logs accessible without proper authorization

### Data Exposure
7. **Sensitive Data Exposure** - Multiple instances of unencrypted sensitive data:
   - **Password hashes exposed in API responses** - `/api/v1/auth/users` and `/api/v1/auth/users/{id}` return password hashes
   - **Passwords logged in plaintext** - Login and registration endpoints log passwords in application logs
   - **Error messages expose sensitive information** - Database errors reveal connection strings, table names, and query details
   - **System information exposure** - `/api/v1/debug/info` exposes environment variables, database credentials, and system paths
   - **User data export** - `/api/v1/debug/users/export` exposes all user data including password hashes and PII
   - **Information disclosure in error messages** - Error messages reveal user existence, database structure, and internal details

## Development

Run with auto-reload:
```bash
uvicorn main:app --reload
```

Run tests:
```bash
pytest
```



Run tests:

```bash

pytest

```






Run tests:

```bash

pytest

```




