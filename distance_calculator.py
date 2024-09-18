import requests
from geopy.distance import great_circle
import mysql.connector

# Function to get distance matrix from OpenRouteService API
def get_openrouteservice_distance_matrix(api_key, locations):
    url = "https://api.openrouteservice.org/v2/matrix/driving-car"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "locations": locations,  # Locations include the origin and destinations
        "metrics": ["distance", "duration"]
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    
    # Print response for debugging
    print("API Working")
    print(response_data)
    
    return response_data

# Function to find nearest ambulance to camera location
def find_nearest_ambulance(camera_location, ambulance_locations, db_config, api_key):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Combine camera location (origin) with ambulance locations (destinations)
    locations = [[camera_location[1], camera_location[0]]]  # OpenRouteService uses [longitude, latitude]
    locations += [[location[2], location[1]] for location in ambulance_locations]  # Append each ambulance location

    distances = get_openrouteservice_distance_matrix(api_key, locations)
    nearest_ambulance = None
    min_distance = float('inf')

    if 'distances' not in distances:
        print("Error: No distances in distance matrix response")
        conn.close()
        return None

    # The first row contains distances from the origin to all destinations
    for i, distance in enumerate(distances['distances'][0][1:], start=1):
        if distance < min_distance:
            min_distance = distance
            nearest_ambulance = ambulance_locations[i - 1]

    conn.close()
    return nearest_ambulance
