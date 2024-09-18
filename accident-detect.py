# main.py

from ultralytics import YOLO
from config import DB_CONFIG, GOOGLE_MAPS_API_KEY, CAMERA_ID,SMS_API_KEY
from db_operations import fetch_camera_location, fetch_ambulance_locations, fetch_phone_number,fetch_coordinates
from distance_calculator import find_nearest_ambulance
from smsSender import send_sms_via_fast2sms

def handle_accident_detection(image_path):
    # Load the YOLO model
    model = YOLO('best.pt')

    # Predict using the model
    results = model.predict(image_path, imgsz=640, conf=0.4, save=True, show=True)

    # Process and print the detection results
    accident_detected = False
    for result in results:
        boxes = result.boxes
        names = result.names

        for box in boxes:
            cls_id = int(box.cls)
            class_name = names[cls_id]
            confidence = float(box.conf)

            print(f"Detected: {class_name} with confidence {confidence:.2f}")

            if class_name in ['severe', 'moderate', 'mild']:

                if class_name == 'severe':
                    print("Accident with Severe")
                    accident_detected = True
                elif class_name == 'moderate':
                    print("Moderate Accident")
                elif class_name == 'mild':
                    print("Mild Accident")
                else:
                    print("Other Detection")

    if accident_detected:
        camera_location = fetch_camera_location(DB_CONFIG, CAMERA_ID)
        if not camera_location:
            print(f"No location found for camera ID {CAMERA_ID}")
            return

        ambulance_locations = fetch_ambulance_locations(DB_CONFIG)
        nearest_ambulance = find_nearest_ambulance(camera_location, ambulance_locations, DB_CONFIG, GOOGLE_MAPS_API_KEY)

        if nearest_ambulance:
            ambulance_id = nearest_ambulance[0]
            phone_number = fetch_phone_number(DB_CONFIG, ambulance_id)
            latitude, longitude = fetch_coordinates(DB_CONFIG, CAMERA_ID)
            print(f"The nearest ambulance's phone number is: {phone_number}")
            google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
            message = f"Accident detected in Camera Number: {CAMERA_ID}\nLocation: {google_maps_url}"
            # message = f"Accident occured"
            print(message)
            send_sms_via_fast2sms(SMS_API_KEY,phone_number,message)
            print("Message sent successfully")
        else:
            print("No ambulance found.")
    else:
        print("No accident detected.")

if __name__ == "__main__":
    image_path = "Accidents.mp4"
    handle_accident_detection(image_path)
