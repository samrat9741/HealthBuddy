import requests
import os
from dotenv import load_dotenv
from math import radians, sin, cos, sqrt, atan2

load_dotenv()

# Load API configuration from environment variables
NOMINATIM_API_URL = os.getenv("NOMINATIM_API_URL", "https://nominatim.openstreetmap.org/search")
OVERPASS_API_URL = os.getenv("OVERPASS_API_URL", "https://overpass-api.de/api/interpreter")
NOMINATIM_EMAIL = os.getenv("NOMINATIM_EMAIL", "")


def search_nearby_facilities(location: str, search_type: str = "all", radius: int = 5000):
    try:
        location = location.strip()
        search_type = search_type.lower()
        
        if not location:
            return {"success": False, "error": "Location is required", "results": []}
        
        geocode_params = {"q": location, "format": "json", "limit": 1}
        if NOMINATIM_EMAIL:
            geocode_params["email"] = NOMINATIM_EMAIL
        
        geocode_response = requests.get(NOMINATIM_API_URL, params=geocode_params, timeout=10)
        if geocode_response.status_code != 200 or not geocode_response.json():
            return {
                "success": False,
                "error": "Could not find location. Please try a different address.",
                "results": []
            }
        
        geocode_data = geocode_response.json()[0]
        lat = float(geocode_data['lat'])
        lon = float(geocode_data['lon'])
        
        results = []
        
        # Search for pharmacies
        if search_type in ["all", "pharmacy"]:
            pharmacy_results = search_overpass(lat, lon, "pharmacy", radius)
            results.extend([{"type": "pharmacy", **r} for r in pharmacy_results])
        
        # Search for hospitals
        if search_type in ["all", "hospital"]:
            hospital_results = search_overpass(lat, lon, "hospital", radius)
            results.extend([{"type": "hospital", **r} for r in hospital_results])
        
        return {
            "success": True,
            "location": geocode_data.get('display_name', location),
            "results": results,
            "count": len(results)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Network error: {str(e)}",
            "results": []
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching nearby locations: {str(e)}",
            "results": []
        }


def search_overpass(lat: float, lon: float, facility_type: str, radius: int = 5000):
    try:
        if facility_type == "pharmacy":
            query = f"""
            [bbox:-90,-180,90,180];
            node["amenity"="pharmacy"](around:{radius},{lat},{lon});
            out center;
            """
            facility_key = "pharmacy"
        else:  # hospital
            query = f"""
            [bbox:-90,-180,90,180];
            (node["amenity"="hospital"](around:{radius},{lat},{lon});
             way["amenity"="hospital"](around:{radius},{lat},{lon}););
            out center;
            """
            facility_key = "hospital"
        
        response = requests.post(OVERPASS_API_URL, data=query, timeout=15)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        results = []
        
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name", f"Unnamed {facility_key.capitalize()}")
            
            # Get coordinates
            if "center" in element:
                coord_lat = element["center"].get("lat", 0)
                coord_lon = element["center"].get("lon", 0)
            else:
                coord_lat = element.get("lat", 0)
                coord_lon = element.get("lon", 0)
            
            # Get address components
            address = tags.get("addr:full", "")
            if not address:
                street = tags.get("addr:street", "")
                city = tags.get("addr:city", "")
                address = f"{street}, {city}".strip(", ")
            
            phone = tags.get("phone", "N/A")
            website = tags.get("website", "")
            opening_hours = tags.get("opening_hours", "Open 24/7")
            
            # Calculate distance
            distance = calculate_distance(lat, lon, coord_lat, coord_lon)
            
            results.append({
                "name": name,
                "address": address or "Address not available",
                "phone": phone,
                "website": website,
                "hours": opening_hours,
                "distance": f"{distance:.1f} km",
                "latitude": coord_lat,
                "longitude": coord_lon
            })
        
        # Sort by distance
        results.sort(key=lambda x: float(x["distance"].split()[0]))
        
        return results[:10]  # Return top 10 results
        
    except Exception as e:
        print(f"Error in search_overpass: {str(e)}")
        return []


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c
