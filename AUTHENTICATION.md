# HealthBuddy - Login & Registration System

## Overview
A complete authentication system has been integrated into your HealthBuddy project that allows users to register and login using their phone number.

## Features

✅ **Phone Number Authentication** - Users can register and login using their phone number
✅ **Secure Password Storage** - Passwords are stored securely (consider hashing in production)
✅ **Form Validation** - Comprehensive client and server-side validation
✅ **Error Handling** - User-friendly error messages
✅ **User Sessions** - User information stored in browser localStorage
✅ **Responsive Design** - Works on all devices

## File Structure

### New Files Created:
- `backend/lib/auth.py` - Backend authentication logic
- `frontend/auth.html` - Login and registration page
- Updated `backend/main.py` - Added authentication endpoints
- Updated `frontend/app.js` - Added auth UI functions
- Updated `frontend/index.html` - Added user menu
- `backend/data/users.json` - User database (auto-created)

## Authentication Endpoints

### 1. Register User
**POST** `/api/auth/register`

**Request:**
```json
{
  "phone": "+1 (555) 123-4567",
  "password": "password123",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Registration successful! You can now login."
}
```

### 2. Login User
**POST** `/api/auth/login`

**Request:**
```json
{
  "phone": "+1 (555) 123-4567",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful!",
  "user": {
    "phone": "1234567890",
    "name": "John Doe",
    "created_at": "2024-12-28T10:30:00"
  }
}
```

### 3. Get User Details
**GET** `/api/auth/user/{phone}`

**Response:**
```json
{
  "success": true,
  "user": {
    "phone": "1234567890",
    "name": "John Doe",
    "created_at": "2024-12-28T10:30:00"
  }
}
```

## How to Use

### 1. **Access Login/Registration Page**
   - Click the "Login" button in the navigation bar
   - Or go to `http://localhost:3000/auth.html`

### 2. **Register a New Account**
   - Click on the "Register" tab
   - Enter your full name, phone number, and password
   - Confirm your password
   - Click "Create Account"
   - You'll be redirected to the login page

### 3. **Login**
   - Enter your phone number and password
   - Click "Login"
   - You'll be redirected to the home page with your account active
   - Your name and phone number will appear in the user menu

### 4. **Logout**
   - Click the account button in the navigation bar
   - Click "Logout"
   - Your session will be cleared

## Phone Number Format

The system accepts phone numbers in various formats:
- `+1 (555) 123-4567`
- `555-123-4567`
- `5551234567`
- `+1 555 123 4567`

The system requires at least 10 digits.

## Password Requirements

- Minimum 6 characters
- Must match confirmation password during registration
- Stored in JSON file (for production, use bcrypt or similar hashing)

## Data Storage

User data is stored in `backend/data/users.json`:

```json
{
  "1234567890": {
    "phone": "1234567890",
    "password": "password123",
    "name": "John Doe",
    "created_at": "2024-12-28T10:30:00",
    "last_login": "2024-12-28T10:35:00"
  }
}
```

## Security Notes

⚠️ **For Development Only**:
- Passwords are currently stored in plain text
- User data is in a JSON file, not a database

**For Production**:
1. Use a proper database (PostgreSQL, MongoDB, etc.)
2. Hash passwords using bcrypt or argon2
3. Implement JWT tokens for session management
4. Add rate limiting to prevent brute force attacks
5. Use HTTPS only
6. Add email verification
7. Implement password reset functionality

## Frontend Integration

The authentication system is integrated with your existing pages:

1. **Navigation Bar**: Shows login button if not authenticated, user account button if authenticated
2. **User Menu**: Displays user name and phone number with logout option
3. **Chat Features**: Available for authenticated users
4. **localStorage**: User data stored for session persistence

## API Integration

All frontend calls to authentication endpoints:

```javascript
// Register
fetch('http://localhost:8000/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ phone, password, name })
})

// Login
fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ phone, password })
})
```

## Testing Credentials

After registration, use your credentials to login:
- **Phone**: Your registered phone number
- **Password**: Your registered password

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection error" | Make sure backend is running on `http://localhost:8000` |
| "Phone number already registered" | Use a different phone number or reset the `data/users.json` file |
| "Invalid phone number" | Phone number must have at least 10 digits |
| "Password must be at least 6 characters" | Use a longer password |
| Users not staying logged in | Check browser localStorage is enabled |

## Next Steps

1. **Add Database**: Replace JSON storage with a database
2. **Password Hashing**: Implement secure password hashing
3. **Email Verification**: Add email confirmation for new accounts
4. **Forgot Password**: Implement password reset functionality
5. **Two-Factor Authentication**: Add SMS or email-based 2FA
6. **Profile Management**: Let users update their profile information
7. **Session Management**: Implement JWT tokens and refresh tokens

## Support

For issues or questions, please check:
- Backend console for server errors
- Browser console (F12) for client-side errors
- Make sure the backend server is running: `python main.py`
