# Field Office Access Guide

## Overview

The QDA Bilingual App now supports field office-based access control, allowing users from different organizational levels to access the application:

- **SFO** (Senior Field Office) - Administrative access
- **LFO** (Local Field Office) - Researcher access  
- **JFO** (Junior Field Office) - Analyst access

## User Roles

### Field Office Types

1. **Senior Field Office (SFO)**
   - Full administrative privileges
   - Can manage all projects and data
   - Role: Admin

2. **Local Field Office (LFO)**
   - Researcher privileges
   - Can create and manage research projects
   - Role: Researcher

3. **Junior Field Office (JFO)**
   - Analyst privileges  
   - Can analyze data and generate reports
   - Role: Analyst

## Authentication

### Login Endpoint

**POST /login**

Login with field office credentials:

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sfo@example.com",
    "password": "sfo123"
  }'
```

**Response:**
```json
{
  "access_token": "sfo@example.com_sfo",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "sfo@example.com",
    "full_name": "Senior Field Officer",
    "field_office": "sfo",
    "role": "admin",
    "is_active": true
  }
}
```

### Get Current User

**GET /users/me?token={access_token}**

Retrieve current user information:

```bash
curl http://localhost:8000/users/me?token=sfo@example.com_sfo
```

## Default Users

The application comes with three pre-configured field office users:

### 1. Senior Field Office (SFO)
- **Email:** sfo@example.com
- **Password:** sfo123
- **Role:** Admin
- **Field Office:** SFO

### 2. Local Field Office (LFO)
- **Email:** lfo@example.com
- **Password:** lfo123
- **Role:** Researcher
- **Field Office:** LFO

### 3. Junior Field Office (JFO)
- **Email:** jfo@example.com
- **Password:** jfo123
- **Role:** Analyst
- **Field Office:** JFO

## API Usage Examples

### Example 1: SFO Login

```bash
# Login as Senior Field Officer
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sfo@example.com",
    "password": "sfo123"
  }'
```

### Example 2: LFO Login

```bash
# Login as Local Field Officer
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "lfo@example.com",
    "password": "lfo123"
  }'
```

### Example 3: JFO Login

```bash
# Login as Junior Field Officer
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jfo@example.com",
    "password": "jfo123"
  }'
```

## Security Notes

⚠️ **Important:** The current implementation uses simple token-based authentication for demonstration purposes. In a production environment, you should:

1. Use JWT (JSON Web Tokens) for secure authentication
2. Hash passwords using bcrypt or similar
3. Implement token expiration and refresh mechanisms
4. Add rate limiting to prevent brute force attacks
5. Use HTTPS for all API communications
6. Store tokens securely (e.g., httpOnly cookies)

## Integration with Frontend

To integrate field office authentication in your React frontend:

```javascript
// Login function
const login = async (email, password) => {
  const response = await fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  
  const data = await response.json();
  
  // Store token and user info
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('user', JSON.stringify(data.user));
  
  return data;
};

// Get current user
const getCurrentUser = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`http://localhost:8000/users/me?token=${token}`);
  return await response.json();
};
```

## Next Steps

1. Implement role-based access control (RBAC) for endpoints
2. Add field office-specific data filtering
3. Create audit logs for field office activities
4. Implement multi-factor authentication for sensitive operations
5. Add field office management endpoints for admins

## Support

For questions or issues related to field office access, please open an issue on GitHub or contact your system administrator.
