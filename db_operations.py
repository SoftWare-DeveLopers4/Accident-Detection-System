# db_operations.py

import mysql.connector

# Function to fetch camera location by camera_id
def fetch_camera_location(db_config, camera_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude FROM camera WHERE camera_id = %s", (camera_id,))
    location = cursor.fetchone()
    conn.close()
    print(location)
    return location

# Function to fetch all ambulance locations
def fetch_ambulance_locations(db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT ambulance_id, latitude, longitude FROM ambulance")
    locations = cursor.fetchall()
    conn.close()
    print(locations)
    return locations

# Function to fetch phone number by ambulance_id
def fetch_phone_number(db_config, ambulance_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT contact FROM ambulance WHERE ambulance_id = %s", (ambulance_id,))
    phone_number = cursor.fetchone()[0]
    conn.close()
    return phone_number

# Function to fetch latitude and longitude by ambulance_id
def fetch_coordinates(db_config, camera_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude FROM camera WHERE camera_id = %s", (camera_id,))
    coordinates = cursor.fetchone()
    conn.close()
    if coordinates:
        return coordinates[0], coordinates[1]
    else:
        return None, None
