import json
import os
from datetime import datetime
import re
from pathlib import Path

# Use a simple JSON file for storing user data (in production, use a database)
USERS_DB_FILE = os.path.join(os.path.dirname(__file__), '../data/users.json')

# Create data directory if it doesn't exist
os.makedirs(os.path.dirname(USERS_DB_FILE), exist_ok=True)

def load_users():
    """Load users from JSON file"""
    if not os.path.exists(USERS_DB_FILE):
        return {}
    try:
        with open(USERS_DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    """Save users to JSON file"""
    os.makedirs(os.path.dirname(USERS_DB_FILE), exist_ok=True)
    with open(USERS_DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def validate_phone(phone):
    """Validate phone number format"""
    # Accept phone numbers with 10+ digits
    phone_digits = re.sub(r'\D', '', phone)
    if len(phone_digits) < 10:
        return False
    return True

def register_user(phone, password, name):
    """Register a new user"""
    # Validate inputs
    if not phone or not password or not name:
        return {"success": False, "message": "All fields are required"}
    
    if not validate_phone(phone):
        return {"success": False, "message": "Invalid phone number. Please enter a valid phone number."}
    
    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters long"}
    
    # Normalize phone number (remove all non-digits)
    phone_normalized = re.sub(r'\D', '', phone)
    
    users = load_users()
    
    # Check if user already exists
    if phone_normalized in users:
        return {"success": False, "message": "Phone number already registered. Please login or use a different number."}
    
    # Create new user
    users[phone_normalized] = {
        "phone": phone_normalized,
        "password": password,  # In production, hash the password!
        "name": name,
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }
    
    save_users(users)
    return {"success": True, "message": "Registration successful! You can now login."}

def login_user(phone, password):
    """Login a user"""
    # Validate inputs
    if not phone or not password:
        return {"success": False, "message": "Phone number and password are required"}
    
    if not validate_phone(phone):
        return {"success": False, "message": "Invalid phone number"}
    
    # Normalize phone number
    phone_normalized = re.sub(r'\D', '', phone)
    
    users = load_users()
    
    # Check if user exists
    if phone_normalized not in users:
        return {"success": False, "message": "Phone number not found. Please register first."}
    
    user = users[phone_normalized]
    
    # Verify password
    if user["password"] != password:
        return {"success": False, "message": "Incorrect password"}
    
    # Update last login
    user["last_login"] = datetime.now().isoformat()
    save_users(users)
    
    return {
        "success": True,
        "message": "Login successful!",
        "user": {
            "phone": user["phone"],
            "name": user["name"],
            "created_at": user["created_at"]
        }
    }

def get_user_by_phone(phone):
    """Get user details by phone number"""
    phone_normalized = re.sub(r'\D', '', phone)
    users = load_users()
    if phone_normalized in users:
        user = users[phone_normalized]
        return {
            "phone": user["phone"],
            "name": user["name"],
            "created_at": user["created_at"]
        }
    return None
