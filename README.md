# Course Registration System - Vulnerable Application
## ACS Security Project

This is a deliberately vulnerable course registration system built for security assessment and educational purposes.

---

## 🎯 Project Overview

A full-stack web application for course registration with **intentionally implemented security vulnerabilities** for:
- Security assessment and penetration testing
- Vulnerability exploitation demonstration
- Security patching exercises

---

## ⚠️ Security Vulnerabilities

This application contains **deliberate security vulnerabilities**. Do NOT deploy to production.

### Implemented Vulnerabilities:

1. **SQL Injection** (Medium)
   - Location: `/api/v1/courses?filter=`
   - Unsanitized SQL query parameter

2. **Reflected XSS** (Low)
   - Location: Course search results
   - User input echoed without sanitization

3. **CSRF** (High)
   - Location: `/api/v1/enrollments`
   - Missing CSRF token validation

4. **Broken Authentication** (High)
   - Weak password policy
   - Insecure session management

---

## 📁 Project Structure

```
Project/
├── docs/                    # Documentation
│   ├── threat_model.md      # Threat model document
│   ├── threat_model.pdf     # Exported PDF
│   ├── architecture.svg     # System architecture diagram
│   └── dataflow.svg         # Data flow diagram
├── recon/                   # Reconnaissance artifacts
│   ├── stack_inventory.md   # Web tech stack enumeration
│   └── api_endpoints.md     # API surface mapping
├── backend/                 # Backend API (FastAPI/Express)
├── frontend/                # Frontend (React)
├── tests/                   # Test suites
├── ARCHITECTURE_AND_TASKS.md
├── STAGE1_RECONNAISSANCE.md
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn
- Git

### Installation

See detailed setup instructions in [SETUP.md](SETUP.md)

**Quick Start:**
```bash
# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
```

### Running the Application

**Option 1: HTTP Mode (Unencrypted - for network analysis)**
```bash
# Terminal 1: Start backend on HTTP
cd backend
USE_HTTP=true python main.py

# Terminal 2: Start frontend (proxies to HTTP backend)
cd frontend
npm run dev:http
```

**Option 2: HTTPS Mode (Misconfigured Certificate)**
```bash
# Terminal 1: Start backend on HTTPS
cd backend
python main.py  # HTTPS by default

# Terminal 2: Start frontend (proxies to HTTPS backend)
cd frontend
npm run dev:https
```

**See [LAUNCH_OPTIONS.md](LAUNCH_OPTIONS.md) for detailed configuration options.**

### GitHub Setup

See [GITHUB_SETUP.md](GITHUB_SETUP.md) for detailed repository setup instructions.

---

## 📚 Documentation

- **Architecture & Tasks**: See `ARCHITECTURE_AND_TASKS.md`
- **Stage 1 Guide**: See `STAGE1_RECONNAISSANCE.md`
- **Threat Model**: See `docs/threat_model.md`

---

## 🔒 Security Testing

This application is designed for security testing. All vulnerabilities are documented and should be:
1. Identified through reconnaissance
2. Exploited to demonstrate impact
3. Patched in later stages

---

## 👥 Team

2-person development team working on:
- Backend development
- Frontend development
- Security vulnerability implementation
- Testing and integration

---

## 📝 License

Educational use only. Not for production deployment.

---

## ⚠️ Disclaimer

This application contains intentional security vulnerabilities for educational purposes. Do not use in production environments or expose to untrusted networks.

