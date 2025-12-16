# Vulnerability Report: Unprotected Admin Endpoint

**Severity:** Critical (CVSS 9.1)
**Type:** Broken Access Control / Missing Authentication
**Endpoint:** `POST /api/v1/admin/courses`

## Description
The administrative endpoint for creating courses lacks any authentication or authorization mechanisms. The function signature defines a database dependency (`get_db`) but omits the user authentication dependency (`get_current_user`).

A comment in the source code explicitly states `# TODO: Add admin authentication check`, indicating this was a known omission during development.

## Impact
* **Unauthorized Access:** Anonymous users can create courses.
* **Data Integrity:** Malicious actors can spam the database with fake courses.
* **Operational Risk:** Attackers can fill course capacity or disrupt scheduling.

## Proof of Concept (PoC)
An attacker can simply send a standard HTTP POST request without any `Authorization` header or Cookies, and the server will process the request.

## Remediation
**Patch:**
1.  Import the authentication dependency (e.g., `get_current_user`).
2.  Add the dependency to the route signature: `user = Depends(get_current_user)`.
3.  Implement a role check to ensure `user.role == "admin"`.