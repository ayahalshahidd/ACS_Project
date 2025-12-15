"""
Test script to verify misconfigured HTTPS certificate vulnerabilities
This script demonstrates how to test the certificate misconfigurations
"""
import ssl
import socket
import requests
from cryptography import x509
from datetime import datetime, timezone
import os

def test_certificate_vulnerabilities():
    """
    Test the misconfigured certificate for various vulnerabilities
    """
    cert_path = os.path.join(os.path.dirname(__file__), "cert.pem")
    
    if not os.path.exists(cert_path):
        print("[!] Certificate not found. Please generate it first:")
        print("    python generate_misconfigured_cert.py")
        return
    
    print("=" * 70)
    print("Testing Misconfigured HTTPS Certificate Vulnerabilities")
    print("=" * 70)
    print()
    
    # Read and parse the certificate
    with open(cert_path, 'rb') as f:
        cert_data = f.read()
        cert = x509.load_pem_x509_certificate(cert_data)
    
    print("1. CERTIFICATE EXPIRATION TEST")
    print("-" * 70)
    # Use UTC-aware datetime methods to avoid deprecation warnings
    now = datetime.now(timezone.utc)
    # Try to use UTC-aware method, fall back to naive datetime
    if hasattr(cert, 'not_valid_after_utc'):
        not_valid_after = cert.not_valid_after_utc
    else:
        # Convert naive datetime to UTC-aware
        not_valid_after_naive = cert.not_valid_after
        not_valid_after = not_valid_after_naive.replace(tzinfo=timezone.utc) if not_valid_after_naive.tzinfo is None else not_valid_after_naive
    
    if now > not_valid_after:
        print("   [VULNERABLE] Certificate is EXPIRED")
        print(f"   Expired on: {not_valid_after}")
        print(f"   Current date: {now}")
        days_expired = (now - not_valid_after).days
        print(f"   Expired {days_expired} days ago")
    else:
        print("   [OK] Certificate is still valid")
    print()
    
    print("2. COMMON NAME (CN) MISMATCH TEST")
    print("-" * 70)
    cn = None
    for attribute in cert.subject:
        if attribute.oid._name == 'commonName':
            cn = attribute.value
            break
    
    if cn:
        print(f"   Certificate CN: {cn}")
        print(f"   Expected CN: localhost")
        if cn != "localhost":
            print("   [VULNERABLE] Common Name does NOT match the server domain")
            print("   Browsers will show 'NET::ERR_CERT_COMMON_NAME_INVALID' error")
        else:
            print("   [OK] Common Name matches")
    print()
    
    print("3. CERTIFICATE ISSUER TEST")
    print("-" * 70)
    issuer = cert.issuer
    subject = cert.subject
    
    if issuer == subject:
        print("   [VULNERABLE] Certificate is SELF-SIGNED")
        print("   Issuer and Subject are the same (self-signed certificate)")
        print("   Browsers will show 'NET::ERR_CERT_AUTHORITY_INVALID' error")
    else:
        print("   [OK] Certificate is signed by a CA")
    print()
    
    print("4. CERTIFICATE KEY SIZE TEST")
    print("-" * 70)
    public_key = cert.public_key()
    key_size = public_key.key_size if hasattr(public_key, 'key_size') else None
    if key_size:
        print(f"   Key size: {key_size} bits")
        if key_size < 2048:
            print("   [VULNERABLE] Key size is below recommended 2048-bit minimum")
        else:
            print("   [OK] Key size meets minimum requirements (2048-bit)")
            print("   Note: OpenSSL requires minimum 2048-bit keys")
    print()
    
    print("5. SIGNATURE ALGORITHM TEST")
    print("-" * 70)
    sig_oid = cert.signature_algorithm_oid
    sig_name = sig_oid._name if hasattr(sig_oid, '_name') else str(sig_oid)
    print(f"   Signature algorithm: {sig_name}")
    if 'sha1' in sig_name.lower() or 'md5' in sig_name.lower():
        print("   [VULNERABLE] Using weak signature algorithm (deprecated)")
    else:
        print("   [OK] Using secure signature algorithm (SHA256)")
        print("   Note: Modern crypto libraries don't support weak algorithms")
    print()
    
    print("6. BROWSER TEST INSTRUCTIONS")
    print("-" * 70)
    print("   To test in a browser:")
    print("   1. Start the backend server: python main.py")
    print("   2. Open browser and navigate to: https://localhost:8000")
    print("   3. You should see certificate warnings:")
    print("      - 'Your connection is not private'")
    print("      - 'NET::ERR_CERT_AUTHORITY_INVALID' (self-signed)")
    print("      - 'NET::ERR_CERT_COMMON_NAME_INVALID' (wrong CN)")
    print("      - 'NET::ERR_CERT_DATE_INVALID' (expired)")
    print("   4. Click 'Advanced' -> 'Proceed to localhost (unsafe)'")
    print("   5. The site will load, demonstrating the vulnerability")
    print()
    
    print("7. COMMAND LINE TEST")
    print("-" * 70)
    print("   Test with curl (will show certificate errors):")
    print("   curl -k https://localhost:8000")
    print("   (The -k flag ignores certificate errors)")
    print()
    print("   Test with openssl:")
    print("   openssl s_client -connect localhost:8000 -showcerts")
    print()
    
    print("=" * 70)
    print("VULNERABILITY SUMMARY")
    print("=" * 70)
    vulnerabilities = []
    if now > not_valid_after:
        vulnerabilities.append("Expired Certificate")
    if cn and cn != "localhost":
        vulnerabilities.append("Wrong Common Name")
    if issuer == subject:
        vulnerabilities.append("Self-Signed Certificate")
    
    if vulnerabilities:
        print("Detected vulnerabilities:")
        for vuln in vulnerabilities:
            print(f"  [X] {vuln}")
    else:
        print("No vulnerabilities detected (unexpected)")
    print()

if __name__ == "__main__":
    test_certificate_vulnerabilities()
