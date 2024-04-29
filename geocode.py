import googlemaps

LATITUDE_KEY="lat"
LONGITUDE_KEY="lng"

def initialize_google_maps(api_key):
    """Initialize the Google Maps client with the provided API key."""
    return googlemaps.Client(key=api_key)

def geocode_address(gmaps, address):
    """Geocode the given address using the Google Maps API and return the latitude and longitude."""
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        return geocode_result[0]['geometry']['location'] 
    return None

def get_latitude_from_geocoded_address(geocode_data):
    """Get the latitude from geocoded address data"""

    if (geocode_address is None):
        return None
    
    if LATITUDE_KEY not in geocode_data:
        print("Warning: No latitude in geocode address!")
        return None

    return geocode_data[LATITUDE_KEY]
    

def get_longitude_from_geocoded_address(geocode_data):
    """Get the longitude from geocoded address data"""

    if (geocode_address is None):
        return None
    
    if LONGITUDE_KEY not in geocode_data:
        print("Warning: No longitude in geocode address!")
        return None

    return geocode_data[LONGITUDE_KEY]
    