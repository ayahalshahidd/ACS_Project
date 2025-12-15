"""
Course Registration System - Main Application
Monolithic FastAPI backend with intentional security vulnerabilities
"""

import asyncio
import sys
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import routes
from routes import auth, courses, enrollments, admin, audit

# Import database setup
from database import init_db

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = FastAPI(
    title="Course Registration System API",
    description="Vulnerable course registration system for security assessment",
    version="1.0.0"
)

# CORS configuration - intentionally permissive for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://localhost:3000", "https://127.0.0.1:3000"],  # VULNERABLE: Allows specific origins (can't use "*" with credentials)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["Courses"])
app.include_router(enrollments.router, prefix="/api/v1/enrollments", tags=["Enrollments"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(audit.router, prefix="/api/v1/audit", tags=["Audit"])

# VULNERABLE: Debug routes that expose sensitive information
from routes import debug
app.include_router(debug.router, prefix="/api/v1/debug", tags=["Debug"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Course Registration System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Database initialization
@app.on_event("startup")
async def startup_event():
    init_db()


if __name__ == "__main__":
    import os
    import sys
    
    # Check if HTTP mode is requested (for network analysis/testing)
    use_http = os.getenv("USE_HTTP", "false").lower() == "true" or "--http" in sys.argv
    
    if use_http:
        # VULNERABLE: Running on HTTP (unencrypted) for network analysis
        # This makes it easy to demonstrate data exposure with Wireshark
        print("[!] VULNERABLE: Running on HTTP (unencrypted)")
        print("    All data transmitted in plaintext - visible in network traffic")
        print("    Use this mode for network analysis with Wireshark/Burp Suite")
        print()
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,  # HTTP port (unencrypted)
            reload=True
        )
    else:
        # VULNERABLE: HTTPS with misconfigured certificate
        # Certificate has multiple misconfigurations:
        # 1. Expired certificate (validity expired 6 months ago)
        # 2. Wrong Common Name (wrong-domain.example.com instead of localhost)
        # 3. Self-signed certificate with mismatched issuer
        # Note: OpenSSL requires minimum 2048-bit keys (weak key size cannot be demonstrated)
        # Note: Modern crypto libraries require SHA256 (weak algos like SHA1/MD5 not supported)
        cert_path = os.path.join(os.path.dirname(__file__), "cert.pem")
        key_path = os.path.join(os.path.dirname(__file__), "key.pem")
        
        # Check if certificates exist, if not, generate them
        if not os.path.exists(cert_path) or not os.path.exists(key_path):
            print("[!] Certificate files not found. Generating misconfigured certificate...")
            from generate_misconfigured_cert import generate_misconfigured_cert
            generate_misconfigured_cert()
        
        # Run with HTTPS using misconfigured certificate
        print("[!] VULNERABLE: Running on HTTPS with misconfigured certificate")
        print("    Certificate is expired, wrong CN, and self-signed")
        print("    For network analysis, use: USE_HTTP=true python main.py")
        print()
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,  # HTTPS port
            ssl_keyfile=key_path,
            ssl_certfile=cert_path,
            reload=True  # Auto-reload on code changes
        )

