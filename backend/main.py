from lib.agent import chat_with_gpt
from lib.counselor import chat_with_counselor
from lib.nearme import search_nearby_facilities
from lib.auth import register_user, login_user, get_user_by_phone
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class RegisterRequest(BaseModel):
    phone: str
    password: str
    name: str

class LoginRequest(BaseModel):
    phone: str
    password: str

class ScheduleAppointmentRequest(BaseModel):
    date: str
    specialist: str

class DirectionsRequest(BaseModel):
    address: str

class NearbySearchRequest(BaseModel):
    location: str
    search_type: str = "all"  # "all", "pharmacy", or "hospital"
    radius: int = 5000  # radius in meters

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        answer = chat_with_gpt(request.message)
        return {"reply": answer.get("text", answer) if isinstance(answer, dict) else answer, "type": "health"}
    except Exception as e:
        return {"reply": f"Error: {str(e)}", "type": "health"}

@app.post("/api/auth/register")
async def register(request: RegisterRequest):
    """Register a new user with phone number"""
    result = register_user(request.phone, request.password, request.name)
    return result

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    """Login user with phone number and password"""
    result = login_user(request.phone, request.password)
    return result

@app.get("/api/auth/user/{phone}")
async def get_user(phone: str):
    """Get user details by phone number"""
    user = get_user_by_phone(phone)
    if user:
        return {"success": True, "user": user}
    return {"success": False, "message": "User not found"}

@app.post("/counselor")
async def counselor_chat(request: ChatRequest):
    try:
        answer = chat_with_counselor(request.message)
        return {"reply": answer.get("text", answer) if isinstance(answer, dict) else answer, "type": "counselor"}
    except Exception as e:
        return {"reply": f"Error: {str(e)}", "type": "counselor"}

@app.post("/api/schedule-appointment")
async def schedule_appointment(request: ScheduleAppointmentRequest):
    try:
        appointment_date = datetime.fromisoformat(request.date)
        confirmation_message = f"Appointment scheduled with {request.specialist} on {appointment_date.strftime('%B %d, %Y at %I:%M %p')}"
        return {
            "success": True,
            "confirmation": confirmation_message,
            "appointmentId": f"APT-{datetime.now().timestamp()}",
            "specialist": request.specialist,
            "date": request.date
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to schedule appointment: {str(e)}"
        }

@app.post("/api/get-directions")
async def get_directions(request: DirectionsRequest):
    try:
        directions_url = f"https://www.google.com/maps/dir/?api=1&destination={request.address.replace(' ', '+')}"
        if GOOGLE_MAPS_API_KEY:
            directions_url += f"&key={GOOGLE_MAPS_API_KEY}"
        return {
            "success": True,
            "url": directions_url,
            "address": request.address
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to generate directions: {str(e)}"
        }

@app.post("/api/search-nearby")
async def search_nearby(request: NearbySearchRequest):
    try:
        result = search_nearby_facilities(request.location, request.search_type, request.radius)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching nearby locations: {str(e)}",
            "results": []
        }
