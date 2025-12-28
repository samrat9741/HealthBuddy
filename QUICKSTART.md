# HealthBuddy Authentication - Quick Setup Guide

## Installation Steps

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Backend Server
```bash
cd backend
python main.py
```

The server will run on `http://localhost:8000`

### 3. Open Frontend
Open `frontend/index.html` in your browser or serve it with a local server:
```bash
# Option 1: Using Python
cd frontend
python -m http.server 3000

# Option 2: Using Node.js http-server
npx http-server frontend -p 3000
```

Access the app at `http://localhost:3000`

## Quick Test

1. **Register**:
   - Click "Login" button
   - Switch to "Register" tab
   - Enter:
     - Name: `Test User`
     - Phone: `555-123-4567`
     - Password: `password123`
   - Click "Create Account"

2. **Login**:
   - Enter Phone: `555-123-4567`
   - Enter Password: `password123`
   - Click "Login"

3. **View Account**:
   - Click "👤 Account" button in navbar
   - See your profile info and logout option

## Project Files Modified/Created

### ✅ New Files:
- `backend/lib/auth.py` - Authentication logic
- `frontend/auth.html` - Login/Register page
- `backend/data/users.json` - User database (auto-created)
- `AUTHENTICATION.md` - Full documentation

### ✅ Modified Files:
- `backend/main.py` - Added auth endpoints
- `frontend/app.js` - Added auth UI functions
- `frontend/index.html` - Added user menu
- `backend/requirements.txt` - Added pydantic

## Architecture

```
HealthBuddy/
├── backend/
│   ├── main.py (Updated with auth endpoints)
│   ├── lib/
│   │   ├── auth.py (NEW - Authentication logic)
│   │   ├── agent.py
│   │   ├── counselor.py
│   │   └── nearme.py
│   ├── data/
│   │   └── users.json (AUTO-CREATED - User storage)
│   └── requirements.txt (Updated)
├── frontend/
│   ├── index.html (Updated - Added user menu)
│   ├── auth.html (NEW - Login/Register page)
│   ├── app.js (Updated - Added auth functions)
│   ├── ctyle.css (Existing styles)
│
└── AUTHENTICATION.md (Complete documentation)
```

## Key Features

✅ **Phone-based Authentication**
✅ **Registration & Login**
✅ **Form Validation**
✅ **User Sessions**
✅ **Logout Functionality**
✅ **Responsive Design**
✅ **Error Handling**

## Important Notes

- Phone numbers must have at least 10 digits
- Passwords must be at least 6 characters
- User data is stored in JSON (use database for production)
- Passwords are plain text (use hashing for production)
- Users are stored in `backend/data/users.json`

## Common Commands

```bash
# Start backend
cd backend
python main.py

# Start frontend (Python)
cd frontend
python -m http.server 3000

# Start frontend (Node.js)
npx http-server frontend -p 3000

# View users (from project root)
cat backend/data/users.json

# Reset users (delete and regenerate)
rm backend/data/users.json
```

## API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/user/{phone}` - Get user details

For detailed API documentation, see `AUTHENTICATION.md`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend not responding | Make sure `python main.py` is running |
| CORS errors | Backend middleware is configured for all origins |
| Users not persisting | Check `backend/data/users.json` exists |
| localStorage not working | Check browser privacy settings |

## Next Steps

1. Test the authentication system
2. Review `AUTHENTICATION.md` for full documentation
3. Customize styling in `frontend/auth.html`
4. Plan production deployment with proper database and security
5. Add additional features (password reset, email verification, etc.)

---

**System Ready!** Your HealthBuddy project now has a complete phone-based authentication system. Happy coding! 🚀
