import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_SECRET_KEY")

def get_access_token(api_key, api_secret):
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise exception for HTTP errors
    return response.json()["access_token"]

def get_hotels(destination):
    
    access_token = get_access_token(API_KEY, API_SECRET)

    url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "cityCode": destination  # Athens IATA city code
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["data"]


destination = 'ATH'
hotels = get_hotels(destination)
for hotel in hotels:
    print(f"Hotel Name: {hotel['name']}, ID: {hotel['hotelId']}, Address: {hotel['address']}")
