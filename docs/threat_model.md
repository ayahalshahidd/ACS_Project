# Threat Model: Course Registration System

## Document Information
- **Version**: 1.0
- **Last Updated**: 2025-12-15
- **System**: Course Registration System API
- **Scope**: Backend API, Frontend Web Application, Database

---

## 1. Key Assets

### 1.1 Data Assets

#### Database
- **SQLite Database** (`database.db`)
  - User credentials (email, password hashes)
  - Student PII (student IDs, emails, names)
  - Course information (codes, descriptions, schedules)
  - Enrollment records (student-course relationships)
  - Audit logs (user actions, timestamps)

#### Personally Identifiable Information (PII)
- **User Data**:
  - Email addresses
  - Student IDs
  - Password hashes (MD5 - vulnerable)
  - User roles (student, instructor, admin)
  - Last login timestamps
  - Account creation dates

- **Enrollment Data**:
  - Student-course associations
  - Enrollment status
  - Enrollment timestamps

#### Sensitive System Information
- Database connection strings
- Environment variables (potentially containing secrets)
- System configuration details
- File system paths

### 1.2 Application Assets

#### Authentication Tokens
- **Session Cookies** (`sid`):
  - Predictable format: `session_{user_id}`
  - Missing HttpOnly flag (accessible via JavaScript)
  - Missing Secure flag (transmitted over HTTP)
  - No SameSite protection

- **JWT Tokens** (`/api/v1/auth/token`):
  - Base64-encoded user data (not properly signed)
  - No expiration mechanism
  - Weak token generation

#### Admin Console
- **Admin Endpoints** (`/api/v1/admin/*`):
  - Course creation/modification
  - Enrollment overrides
  - Administrative actions
  - **Vulnerability**: Insufficient authorization checks

#### API Documentation
- **Swagger UI** (`/docs`):
  - Complete API endpoint listing
  - Request/response schemas
  - Parameter documentation
  - **Risk**: Information disclosure to attackers

- **OpenAPI Schema** (`/openapi.json`):
  - Machine-readable API specification
  - All endpoints and methods exposed

### 1.3 Infrastructure Assets

#### Server Configuration
- **HTTPS Certificates**:
  - Self-signed certificates
  - Expired certificates
  - Wrong Common Name (CN mismatch)
  - **Risk**: Man-in-the-Middle (MITM) attacks

#### Network Traffic
- **Unencrypted HTTP** (when `USE_HTTP=true`):
  - All API requests/responses in plaintext
  - Credentials transmitted unencrypted
  - Session cookies exposed

---

## 2. Potential Attackers

### 2.1 Student (Regular User)
- **Access Level**: Authenticated user with student role
- **Knowledge**: Basic user of the system
- **Motivation**: 
  - Enroll in restricted courses
  - View other students' information
  - Modify own enrollment records
- **Capabilities**:
  - Access to student endpoints
  - Can make authenticated API requests
  - Limited to own data (in theory)
- **Risk Level**: Medium

### 2.2 External Attacker
- **Access Level**: Unauthenticated or authenticated with limited privileges
- **Knowledge**: Security testing knowledge, common attack techniques
- **Motivation**:
  - Data exfiltration (PII, credentials)
  - System compromise
  - Service disruption
  - Financial gain (selling stolen data)
- **Capabilities**:
  - Network access to the application
  - Can perform reconnaissance
  - Can exploit public-facing vulnerabilities
  - Can intercept network traffic
- **Risk Level**: High

### 2.3 Malicious Insider
- **Access Level**: Authenticated user (student, instructor, or admin)
- **Knowledge**: Internal system knowledge, legitimate access
- **Motivation**:
  - Privilege escalation (student → admin)
  - Unauthorized data access
  - Sabotage
  - Personal gain
- **Capabilities**:
  - Legitimate system access
  - Knowledge of internal processes
  - Can bypass some security controls
  - Can perform authorized actions maliciously
- **Risk Level**: Critical

### 2.4 Instructor
- **Access Level**: Authenticated user with instructor role
- **Knowledge**: System user, may have limited technical knowledge
- **Motivation**:
  - Access student data beyond scope
  - Modify course information
  - View audit logs
- **Capabilities**:
  - Access to instructor-specific endpoints
  - Can view course enrollments
- **Risk Level**: Medium-High

---

## 3. Attack Goals

### 3.1 Data Exfiltration
- **Target**: PII, password hashes, enrollment data, audit logs
- **Methods**:
  - SQL Injection to extract database contents
  - Broken Access Control to access unauthorized endpoints
  - Information Disclosure vulnerabilities
  - Network interception (unencrypted HTTP)
- **Impact**: 
  - Privacy violation
  - Identity theft
  - Regulatory compliance violations (GDPR, FERPA)
  - Reputation damage

### 3.2 Privilege Escalation
- **Target**: Admin console, administrative endpoints
- **Methods**:
  - Session hijacking (predictable session IDs)
  - Broken authentication (weak password hashing)
  - Access control bypass
  - Token manipulation (weak JWT implementation)
- **Impact**:
  - Unauthorized administrative actions
  - System compromise
  - Complete data access
  - Service disruption

### 3.3 Denial of Service (DoS)
- **Target**: API availability, database performance
- **Methods**:
  - SQL Injection with resource-intensive queries
  - Brute force login attempts (no rate limiting)
  - Resource exhaustion attacks
  - Network flooding
- **Impact**:
  - Service unavailability
  - Performance degradation
  - User experience disruption
  - Business continuity issues

### 3.4 Data Manipulation
- **Target**: Course data, enrollment records, user accounts
- **Methods**:
  - CSRF attacks on enrollment endpoints
  - SQL Injection to modify database
  - Unauthorized admin actions
- **Impact**:
  - Data integrity compromise
  - Unauthorized course enrollments
  - Academic record tampering

### 3.5 Session Hijacking
- **Target**: User sessions, authentication tokens
- **Methods**:
  - Predictable session ID guessing
  - Cookie theft via XSS
  - Network interception (unencrypted cookies)
- **Impact**:
  - Account takeover
  - Unauthorized actions on behalf of users
  - Identity impersonation

---

## 4. Top-10 Attack Surfaces

### 4.1 SQL Injection - `/api/v1/courses` (GET)
- **Vulnerability**: Unsanitized `filter` parameter allows direct SQL execution
- **Attack Vector**: `GET /api/v1/courses?filter=1=1 OR 1=1--`
- **Impact**: 
  - Complete database read access
  - Potential data exfiltration
  - Database structure disclosure
- **Severity**: **Critical**
- **CWE**: CWE-89 (SQL Injection)

### 4.2 Broken Authentication - `/api/v1/auth/login` (POST)
- **Vulnerability**: 
  - MD5 password hashing (cryptographically broken)
  - No rate limiting
  - Predictable session IDs (`session_{user_id}`)
  - Missing cookie security flags
- **Attack Vector**: 
  - Brute force attacks
  - Password hash cracking
  - Session ID prediction
- **Impact**: 
  - Account compromise
  - Privilege escalation
  - Session hijacking
- **Severity**: **Critical**
- **CWE**: CWE-287 (Authentication Bypass), CWE-798 (Hard-coded Credentials)

### 4.3 CSRF - `/api/v1/enrollments` (POST)
- **Vulnerability**: No CSRF token validation on state-changing operations
- **Attack Vector**: Malicious website making cross-origin POST requests
- **Impact**: 
  - Unauthorized enrollment actions
  - Data manipulation
  - User action hijacking
- **Severity**: **High**
- **CWE**: CWE-352 (Cross-Site Request Forgery)

### 4.4 Broken Access Control - `/api/v1/audit` (GET)
- **Vulnerability**: Audit logs accessible without proper authorization
- **Attack Vector**: Any authenticated user can access audit logs
- **Impact**: 
  - Information disclosure
  - User activity monitoring
  - Privacy violation
- **Severity**: **High**
- **CWE**: CWE-284 (Improper Access Control)

### 4.5 Information Disclosure - `/api/v1/debug/*` (GET)
- **Vulnerability**: Debug endpoints expose sensitive system information
- **Endpoints**:
  - `/api/v1/debug/info` - System info, environment variables, database connection strings
  - `/api/v1/debug/users/export` - All user data including password hashes
- **Attack Vector**: Direct endpoint access
- **Impact**: 
  - Complete system information disclosure
  - All user credentials exposed
  - Database connection details leaked
- **Severity**: **Critical**
- **CWE**: CWE-209 (Information Exposure)

### 4.6 Weak Access Control - `/api/v1/admin/*` (POST/GET)
- **Vulnerability**: Admin endpoints lack proper authorization checks
- **Endpoints**:
  - `/api/v1/admin/courses` (POST) - Create courses
  - `/api/v1/admin/courses/{course_id}` (GET) - Admin course access
  - `/api/v1/admin/enrollments/override` (POST) - Override enrollments
- **Attack Vector**: 
  - Direct endpoint access with admin header (`X-Admin-Access`)
  - Bypass authorization checks
- **Impact**: 
  - Unauthorized administrative actions
  - Course manipulation
  - Enrollment overrides
- **Severity**: **Critical**
- **CWE**: CWE-284 (Improper Access Control)

### 4.7 Weak Token Generation - `/api/v1/auth/token` (POST)
- **Vulnerability**: 
  - Base64-encoded user data (not properly signed)
  - No expiration mechanism
  - Weak token format
- **Attack Vector**: 
  - Token decoding and manipulation
  - Token replay attacks
  - Long-lived sessions
- **Impact**: 
  - Token forgery
  - Unauthorized API access
  - Session persistence
- **Severity**: **High**
- **CWE**: CWE-326 (Inadequate Encryption Strength)

### 4.8 Information Disclosure - Error Messages
- **Vulnerability**: Detailed error messages expose database structure
- **Location**: `/api/v1/courses/{course_id}` (GET)
- **Attack Vector**: Invalid course ID requests
- **Impact**: 
  - Database schema disclosure
  - Query structure exposure
  - Attack surface expansion
- **Severity**: **Medium**
- **CWE**: CWE-209 (Information Exposure)

### 4.9 Misconfigured HTTPS/TLS
- **Vulnerability**: 
  - Self-signed certificates
  - Expired certificates
  - Wrong Common Name (CN mismatch)
  - Optional HTTP mode (unencrypted)
- **Attack Vector**: 
  - Man-in-the-Middle (MITM) attacks
  - Certificate validation bypass
  - Network traffic interception
- **Impact**: 
  - Credential interception
  - Session cookie theft
  - Data exposure in transit
- **Severity**: **High**
- **CWE**: CWE-295 (Improper Certificate Validation)

### 4.10 Insecure Session Management
- **Vulnerability**: 
  - Predictable session IDs
  - Missing HttpOnly flag
  - Missing Secure flag
  - No SameSite protection
- **Location**: All authenticated endpoints
- **Attack Vector**: 
  - Session ID prediction
  - XSS-based cookie theft
  - Network interception
- **Impact**: 
  - Session hijacking
  - Account takeover
  - Unauthorized access
- **Severity**: **High**
- **CWE**: CWE-384 (Session Fixation), CWE-613 (Insufficient Session Expiration)

---

## 5. Attack Surface Summary

| # | Attack Surface | Endpoint/Service | Severity | Primary Goal |
|---|----------------|------------------|----------|--------------|
| 1 | SQL Injection | `GET /api/v1/courses?filter=` | Critical | Data Exfiltration |
| 2 | Broken Authentication | `POST /api/v1/auth/login` | Critical | Privilege Escalation |
| 3 | CSRF | `POST /api/v1/enrollments` | High | Data Manipulation |
| 4 | Broken Access Control | `GET /api/v1/audit` | High | Data Exfiltration |
| 5 | Information Disclosure | `GET /api/v1/debug/*` | Critical | Data Exfiltration |
| 6 | Weak Access Control | `POST /api/v1/admin/*` | Critical | Privilege Escalation |
| 7 | Weak Token Generation | `POST /api/v1/auth/token` | High | Privilege Escalation |
| 8 | Error Message Disclosure | `GET /api/v1/courses/{id}` | Medium | Information Gathering |
| 9 | Misconfigured HTTPS | Server Configuration | High | Data Exfiltration |
| 10 | Insecure Sessions | All Authenticated Endpoints | High | Session Hijacking |

---

## 6. Threat Scenarios

### Scenario 1: SQL Injection Data Exfiltration
1. **Attacker**: External attacker
2. **Goal**: Extract all user credentials and PII
3. **Method**: 
   - Exploit SQL injection in `/api/v1/courses?filter=`
   - Extract user table: `filter=1=1 UNION SELECT * FROM users--`
   - Extract password hashes and crack MD5 hashes
4. **Impact**: Complete user database compromise

### Scenario 2: Privilege Escalation via Session Hijacking
1. **Attacker**: Student user
2. **Goal**: Gain admin access
3. **Method**:
   - Predict admin session ID: `session_1` (assuming admin is user ID 1)
   - Use predictable session cookie to impersonate admin
   - Access admin endpoints
4. **Impact**: Unauthorized administrative control

### Scenario 3: CSRF Enrollment Manipulation
1. **Attacker**: External attacker
2. **Goal**: Enroll users in courses without consent
3. **Method**:
   - Create malicious website
   - Embed form that POSTs to `/api/v1/enrollments`
   - Trick authenticated user to visit malicious site
4. **Impact**: Unauthorized enrollment actions

### Scenario 4: Debug Endpoint Information Disclosure
1. **Attacker**: External attacker
2. **Goal**: System reconnaissance and credential theft
3. **Method**:
   - Access `/api/v1/debug/info` for system information
   - Access `/api/v1/debug/users/export` for all user data
   - Extract password hashes and crack them
4. **Impact**: Complete system and user data compromise

### Scenario 5: MITM Attack via Misconfigured Certificate
1. **Attacker**: Network-level attacker
2. **Goal**: Intercept credentials and session cookies
3. **Method**:
   - Set up proxy with self-signed certificate
   - Exploit certificate validation bypass
   - Intercept all HTTPS traffic
4. **Impact**: Credential and session theft

---

## 7. Risk Assessment Matrix

| Threat | Likelihood | Impact | Risk Score | Priority |
|--------|------------|--------|------------|----------|
| SQL Injection | High | Critical | **9** | P1 |
| Broken Authentication | High | Critical | **9** | P1 |
| Debug Endpoint Exposure | Medium | Critical | **6** | P1 |
| Admin Access Control | Medium | Critical | **6** | P1 |
| CSRF | High | High | **6** | P1 |
| Weak Token Generation | Medium | High | **4** | P2 |
| Misconfigured HTTPS | Medium | High | **4** | P2 |
| Insecure Sessions | Medium | High | **4** | P2 |
| Error Disclosure | Low | Medium | **2** | P3 |
| Audit Log Exposure | Low | Medium | **2** | P3 |

**Priority Levels:**
- **P1**: Critical - Address immediately
- **P2**: High - Address soon
- **P3**: Medium - Address when possible

---

## 8. Mitigation Recommendations

### Immediate Actions (P1)
1. **Fix SQL Injection**: Use parameterized queries
2. **Strengthen Authentication**: Implement bcrypt/argon2, add rate limiting
3. **Remove Debug Endpoints**: Disable in production
4. **Implement Access Control**: Proper authorization checks on admin endpoints
5. **Add CSRF Protection**: Implement CSRF tokens

### Short-term Actions (P2)
1. **Fix Token Generation**: Use proper JWT with signing and expiration
2. **Secure HTTPS**: Use valid certificates, enforce HTTPS
3. **Secure Sessions**: Add HttpOnly, Secure, SameSite flags

### Long-term Actions (P3)
1. **Improve Error Handling**: Generic error messages
2. **Restrict Audit Logs**: Proper authorization checks

---

## 9. References

- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **CWE Database**: https://cwe.mitre.org/
- **API Endpoints**: See `recon/api_endpoints.md`
- **Stack Inventory**: See `recon/stack_inventory.md`

---

**Document Status**: Active
**Next Review**: After vulnerability remediation
