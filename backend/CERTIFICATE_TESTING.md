# Testing Misconfigured HTTPS Certificate Vulnerabilities

This guide explains how to test and demonstrate the misconfigured HTTPS certificate vulnerabilities in the application.

## Certificate Misconfigurations

The certificate has the following intentional misconfigurations:

1. **Expired Certificate** - Valid from 1 year ago to 6 months ago (expired)
2. **Wrong Common Name** - CN is `wrong-domain.example.com` instead of `localhost`
3. **Self-Signed Certificate** - Issuer and Subject are the same
4. **Weak Key Size** - 2048-bit (minimum required by OpenSSL, but still vulnerable if smaller)

## Testing Methods

### Method 1: Automated Test Script

Run the test script to verify all vulnerabilities:

```bash
cd backend
python test_certificate.py
```

This will check:
- Certificate expiration status
- Common Name mismatch
- Self-signed status
- Key size
- Signature algorithm

### Method 2: Browser Testing

1. **Start the backend server:**
   ```bash
   cd backend
   python main.py
   ```

2. **Open your browser** and navigate to:
   ```
   https://localhost:8000
   ```

3. **Expected Browser Warnings:**
   - Chrome/Edge: "Your connection is not private"
     - Error: `NET::ERR_CERT_AUTHORITY_INVALID` (self-signed)
     - Error: `NET::ERR_CERT_COMMON_NAME_INVALID` (wrong CN)
     - Error: `NET::ERR_CERT_DATE_INVALID` (expired)
   
   - Firefox: "Warning: Potential Security Risk Ahead"
     - Error: `SEC_ERROR_UNKNOWN_ISSUER` (self-signed)
     - Error: `SSL_ERROR_BAD_CERT_DOMAIN` (wrong CN)
     - Error: `SEC_ERROR_EXPIRED_CERTIFICATE` (expired)

4. **Accept the certificate** (for testing):
   - Click "Advanced" → "Proceed to localhost (unsafe)"
   - This demonstrates that users can bypass certificate warnings

### Method 3: Command Line Testing

#### Using curl:
```bash
# Without -k flag (will show certificate errors)
curl https://localhost:8000

# With -k flag (ignores certificate errors - demonstrates vulnerability)
curl -k https://localhost:8000
```

#### Using openssl (if installed):
```bash
# Connect and show certificate details
openssl s_client -connect localhost:8000 -showcerts

# Check certificate expiration
openssl x509 -in cert.pem -noout -dates

# Check certificate subject (CN)
openssl x509 -in cert.pem -noout -subject

# Check certificate issuer
openssl x509 -in cert.pem -noout -issuer
```

**Note:** If openssl is not installed on Windows, use the Python test script instead:
```bash
cd backend
python test_certificate.py
```

Or use Python to inspect the certificate directly:
```python
from cryptography import x509
with open('cert.pem', 'rb') as f:
    cert = x509.load_pem_x509_certificate(f.read())
    print(f"Subject: {cert.subject}")
    print(f"Issuer: {cert.issuer}")
    print(f"Valid from: {cert.not_valid_before}")
    print(f"Valid until: {cert.not_valid_after}")
```

#### Using Python requests:
```python
import requests

# This will fail due to certificate errors
try:
    response = requests.get('https://localhost:8000')
except requests.exceptions.SSLError as e:
    print(f"SSL Error (expected): {e}")

# This will work but ignores certificate validation (VULNERABLE)
response = requests.get('https://localhost:8000', verify=False)
print("Request succeeded (certificate validation bypassed)")
```

### Method 4: Certificate Details Inspection

#### Using Python (Windows-friendly, no openssl required):
```bash
cd backend
python inspect_cert.py
```

This Python script provides the same information as openssl commands but works on Windows without requiring openssl installation.

#### Using openssl (if installed):
```bash
cd backend

# View certificate information
openssl x509 -in cert.pem -text -noout

# Check specific fields
openssl x509 -in cert.pem -noout -subject -issuer -dates
```

Expected output will show:
- **Subject CN**: `wrong-domain.example.com` (wrong!)
- **Issuer**: Same as Subject (self-signed)
- **Validity**: Expired dates

## Security Impact

### Why These Misconfigurations Are Vulnerable:

1. **Expired Certificate:**
   - Certificate is no longer valid
   - Browsers will warn users
   - Could indicate abandoned or unmaintained service

2. **Wrong Common Name:**
   - Certificate doesn't match the domain
   - Indicates potential man-in-the-middle attack
   - Users cannot verify they're connecting to the correct server

3. **Self-Signed Certificate:**
   - Not issued by a trusted Certificate Authority (CA)
   - No third-party validation
   - Users must manually trust the certificate
   - Vulnerable to certificate spoofing

4. **Combined Effect:**
   - Multiple misconfigurations compound the risk
   - Users may become desensitized to warnings
   - Attackers can create similar certificates to impersonate the server

## Demonstration for Security Assessment

To demonstrate these vulnerabilities in a security assessment:

1. **Document the misconfigurations** using `test_certificate.py`
2. **Show browser warnings** with screenshots
3. **Demonstrate the impact:**
   - Show how users can bypass warnings
   - Explain the security risks
   - Show how an attacker could exploit this

4. **Recommended Fixes:**
   - Use a valid certificate from a trusted CA
   - Ensure CN matches the server domain
   - Keep certificates up to date
   - Use proper certificate management

## Testing Checklist

- [ ] Certificate is expired (verified by test script)
- [ ] Common Name doesn't match localhost (verified by test script)
- [ ] Certificate is self-signed (verified by test script)
- [ ] Browser shows certificate warnings
- [ ] Users can bypass warnings (demonstrates vulnerability)
- [ ] Certificate details can be inspected via command line
- [ ] API requests work after accepting certificate

## Notes

- Modern browsers and tools will flag these misconfigurations
- This is intentional for security testing/education purposes
- In production, always use valid certificates from trusted CAs
- Certificate misconfigurations are a common security issue in real-world applications


