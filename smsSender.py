import requests

def send_sms_via_fast2sms(api_key, phone_number, message):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "message": message,
        "language": "english",
        "route": "q",
        "numbers": phone_number,
    }
    headers = {
        'authorization': api_key,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    response = requests.post(url, data=payload, headers=headers)
    
    return response.json()


