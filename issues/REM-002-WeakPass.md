# Remediation Ticket: REM-002 (Broken Authentication)

## Vulnerability Description
The authentication system used `hashlib.md5` for password storage, which is vulnerable to rainbow table attacks and collisions. Additionally, session management relied on insecure cookies accessible to JavaScript.

## Root Cause Analysis
- **Hashing:** Usage of deprecated MD5 algorithm.
- **Cookies:** Missing `HttpOnly` and `SameSite` flags.

## Implemented Fix
- **Algorithm:** Migrated to **Bcrypt** (via `passlib`).
- **Session:** Implemented **JWT** tokens signed with HS256.
- **Transport:** Enforced `HttpOnly=True` and `SameSite='Lax'` on cookies.

## Verification
- **Test:** `tests/security/pass_hash_test.py`
- **Result:** Passwords are now stored as `$2b$12$...` (Bcrypt) strings.