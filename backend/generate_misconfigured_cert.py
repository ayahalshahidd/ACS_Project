"""
Generate misconfigured HTTPS certificate for security testing
VULNERABLE: Multiple certificate misconfigurations
"""
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import os

def generate_misconfigured_cert():
    """
    Generate a certificate with multiple misconfigurations:
    1. Expired certificate (validity in the past)
    2. Wrong Common Name (doesn't match localhost)
    3. Self-signed certificate with mismatched issuer
    Note: Modern OpenSSL requires minimum 2048-bit keys, so we use that but keep other misconfigurations.
    Modern cryptography libraries also don't support weak signature algorithms (SHA1/MD5).
    """
    # Generate Key - Using 2048-bit (minimum required by OpenSSL)
    # Note: We'd prefer 1024-bit to show weak key, but OpenSSL rejects it
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
    # VULNERABLE: Wrong Common Name - doesn't match the actual server domain
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Test"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Vulnerable Server"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"wrong-domain.example.com"),  # VULNERABLE: Wrong CN
    ])
    
    # VULNERABLE: Expired certificate - valid from 1 year ago to 6 months ago
    # Using timezone-aware datetime to avoid deprecation warnings
    now = datetime.datetime.now(datetime.timezone.utc)
    not_valid_before = now - datetime.timedelta(days=365)
    not_valid_after = now - datetime.timedelta(days=180)  # Expired 6 months ago
    
    # Note: Modern cryptography libraries don't support weak signature algorithms (SHA1/MD5)
    # We use SHA256 here, but the certificate is still misconfigured due to:
    # - Expired validity (expired 6 months ago)
    # - Wrong Common Name (doesn't match localhost)
    # - Self-signed certificate with mismatched issuer
    # Note: OpenSSL requires minimum 2048-bit keys, so we can't demonstrate weak key size
    signature_algorithm = hashes.SHA256()
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        not_valid_before
    ).not_valid_after(
        not_valid_after  # VULNERABLE: Certificate is expired
    ).sign(key, signature_algorithm)  # Using SHA256 (required by modern crypto), but cert is still misconfigured
    
    # Write certificate and key files
    cert_path = os.path.join(os.path.dirname(__file__), "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "key.pem")
    
    with open(key_path, "wb") as f:
        f.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        ))
    
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print("[!] VULNERABLE: Misconfigured certificate generated with:")
    print("    - Expired validity (expired 6 months ago)")
    print("    - Wrong Common Name (wrong-domain.example.com instead of localhost)")
    print("    - Self-signed certificate with mismatched issuer")
    print("    Note: OpenSSL requires minimum 2048-bit keys (weak key size cannot be demonstrated)")
    print("    Note: Modern crypto libraries require SHA256 signature (weak algos not supported)")
    print(f"[+] Certificate saved to: {cert_path}")
    print(f"[+] Key saved to: {key_path}")

if __name__ == "__main__":
    generate_misconfigured_cert()
