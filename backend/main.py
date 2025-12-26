from lib.agent import chat_with_gpt
from lib.counselor import chat_with_counselor
from lib.nearme import search_nearby_facilities
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load API configuration from environment variables
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
    """Handle chat requests from the frontend"""
    try:
        answer = chat_with_gpt(request.message)
        return {"reply": answer.get("text", answer) if isinstance(answer, dict) else answer, "type": "health"}
    except Exception as e:
        return {"reply": f"Error: {str(e)}", "type": "health"}

@app.post("/counselor")
async def counselor_chat(request: ChatRequest):
    """Handle mental health counselor chat requests from the frontend"""
    try:
        answer = chat_with_counselor(request.message)
        return {"reply": answer.get("text", answer) if isinstance(answer, dict) else answer, "type": "counselor"}
    except Exception as e:
        return {"reply": f"Error: {str(e)}", "type": "counselor"}

@app.post("/api/schedule-appointment")
async def schedule_appointment(request: ScheduleAppointmentRequest):
    """
    Schedule a medical appointment
    """
    try:
        # Here you would integrate with a real appointment scheduling system
        # For now, we'll return a confirmation
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
    """
    Get Google Maps directions URL
    """
    try:
        directions_url = f"https://www.google.com/maps/dir/?api=1&destination={request.address.replace(' ', '+')}"
        
        # Add API key if available
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
    """
    Search for nearby pharmacies and hospitals using Overpass API (OpenStreetMap)
    """
    try:
        result = search_nearby_facilities(request.location, request.search_type, request.radius)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching nearby locations: {str(e)}",
            "results": []
        }

def main():
    print("I am Health-Buddy, Your nurse! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        answer = chat_with_gpt(user_input)
        print("Health-Buddy:", answer)

if __name__ == "__main__":
    main()
