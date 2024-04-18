import googlemaps
from datetime import datetime

def initialize_google_maps(api_key):
    """Initialize the Google Maps client with the provided API key."""
    return googlemaps.Client(key=api_key)

def geocode_address(gmaps, address):
    """Geocode the given address using the Google Maps API and return the latitude and longitude."""
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        return geocode_result[0]['geometry']['location'] 
    return None
