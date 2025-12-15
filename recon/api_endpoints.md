# API Endpoints Discovery Report

## Reconnaissance Date
2025-12-15 23:15:15

## Target
- **Base URL**: http://localhost:8000
- **API Title**: Course Registration System API
- **API Version**: 1.0.0
- **Discovery Method**: OpenAPI schema (/openapi.json)

## API Endpoints

### Admin

| Path | Method | Summary |
|------|--------|---------|
| /api/v1/admin/enrollments/override | POST | Override Enrollment |
| /api/v1/admin/courses/{course_id} | GET | Get Course Admin |
| /api/v1/admin/courses | POST | Create Course |

### Audit

| Path | Method | Summary |
|------|--------|---------|
| /api/v1/audit | GET | Get Audit Logs |

### Authentication

| Path | Method | Summary |
|------|--------|---------|
| /api/v1/auth/token | POST | Get Token |
| /api/v1/auth/reset-password | POST | Reset Password |
| /api/v1/auth/login | POST | Login |
| /api/v1/auth/logout | POST | Logout |

### Courses

| Path | Method | Summary |
|------|--------|---------|
| /api/v1/courses/{course_id} | GET | Get Course |
| /api/v1/courses | GET | Get Courses |

### Debug

| Path | Method | Summary |
|------|--------|---------|
| /api/v1/debug/users/export | GET | Export All Users |
| /api/v1/debug/info | GET | Get System Info |

### Enrollments

| Path | Method | Summary |
|------|--------|---------|
| /api/v1/enrollments/{enrollment_id} | DELETE | Drop Enrollment |
| /api/v1/enrollments | GET | Get Enrollments |
| /api/v1/enrollments | POST | Create Enrollment |

### Other

| Path | Method | Summary |
|------|--------|---------|
| /health | GET | Health Check |
| / | GET | Root |

## Detailed Endpoint Information

### /

**GET /**

- **Summary**: Root
- **Description**: Root endpoint
- **Responses**:
  - 200 : Successful Response

### /api/v1/admin/courses

**POST /api/v1/admin/courses**

- **Summary**: Create Course
- **Description**: Create course (admin only)
- **Request Body**: Required
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

### /api/v1/admin/courses/{course_id}

**GET /api/v1/admin/courses/{course_id}**

- **Summary**: Get Course Admin
- **Description**: Get course details (admin)
- **Parameters**:
  - $(@{name=course_id; in=path; required=True; schema=}.name) (integer, required)
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

### /api/v1/admin/enrollments/override

**POST /api/v1/admin/enrollments/override**

- **Summary**: Override Enrollment
- **Description**: Override enrollment (admin only)
- **Parameters**:
  - $(@{name=enrollment_id; in=query; required=True; schema=}.name) (integer, required)
  - $(@{name=action; in=query; required=True; schema=}.name) (string, required)
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

### /api/v1/audit

**GET /api/v1/audit**

- **Summary**: Get Audit Logs
- **Description**: Get audit logs
VULNERABLE: Missing access control - should require admin role
- **Parameters**:
  - $(@{name=user; in=query; required=False; schema=; description=Filter by user ID}.name) (unknown, optional)
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

### /api/v1/auth/login

**POST /api/v1/auth/login**

- **Summary**: Login
- **Description**: Login endpoint
VULNERABLE: Weak password hashing, no rate limiting, session fixation
- **Request Body**: Required
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

### /api/v1/auth/logout

**POST /api/v1/auth/logout**

- **Summary**: Logout
- **Description**: Logout endpoint
- **Responses**:
  - 200 : Successful Response

### /api/v1/auth/reset-password

**POST /api/v1/auth/reset-password**

- **Summary**: Reset Password
- **Description**: Password reset endpoint
VULNERABLE: Weak reset mechanism
- **Request Body**: Required
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

### /api/v1/auth/token

**POST /api/v1/auth/token**

- **Summary**: Get Token
- **Description**: Generate JWT token for API clients
VULNERABLE: Weak token signing, no expiration
- **Request Body**: Required
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

### /api/v1/courses

**GET /api/v1/courses**

- **Summary**: Get Courses
- **Description**: Get courses with optional filter
VULNERABLE: SQL Injection - filter parameter is unsanitized
Example attack: ?filter=1=1 OR 1=1--
- **Parameters**:
  - $(@{name=filter; in=query; required=False; schema=; description=Filter courses - VULNERABLE: SQL Injection}.name) (unknown, optional)
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

### /api/v1/courses/{course_id}

**GET /api/v1/courses/{course_id}**

- **Summary**: Get Course
- **Description**: Get course details
VULNERABLE: Error messages expose sensitive database information
- **Parameters**:
  - $(@{name=course_id; in=path; required=True; schema=}.name) (integer, required)
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

### /api/v1/debug/info

**GET /api/v1/debug/info**

- **Summary**: Get System Info
- **Description**: Get system information
VULNERABLE: Exposes sensitive system and configuration information
This endpoint should be disabled in production
- **Responses**:
  - 200 : Successful Response

### /api/v1/debug/users/export

**GET /api/v1/debug/users/export**

- **Summary**: Export All Users
- **Description**: Export all user data
VULNERABLE: Exposes all sensitive user data including password hashes
This should require admin authentication and proper authorization
- **Responses**:
  - 200 : Successful Response

### /api/v1/enrollments

**GET /api/v1/enrollments**

- **Summary**: Get Enrollments
- **Description**: Get enrollments
- **Parameters**:
  - $(@{name=user_id; in=query; required=False; schema=}.name) (unknown, optional)
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

**POST /api/v1/enrollments**

- **Summary**: Create Enrollment
- **Description**: VULNERABLE: CSRF
Now accepts standard HTML Form data, making it easy to exploit.
- **Request Body**: Required
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

### /api/v1/enrollments/{enrollment_id}

**DELETE /api/v1/enrollments/{enrollment_id}**

- **Summary**: Drop Enrollment
- **Description**: Drop enrollment
- **Parameters**:
  - $(@{name=enrollment_id; in=path; required=True; schema=}.name) (integer, required)
- **Responses**:
  - 200 : Successful Response
  - 422 : Validation Error

### /health

**GET /health**

- **Summary**: Health Check
- **Description**: Health check endpoint
- **Responses**:
  - 200 : Successful Response

## Summary

- **Total API Paths**: 16
- **Total Endpoints**: 17
- **API Groups**: 7

## Notes

- Endpoints discovered from OpenAPI schema at /openapi.json`n- Interactive documentation available at /docs (Swagger UI)
- Alternative documentation at /redoc (ReDoc)
- Server must be running to access endpoints

