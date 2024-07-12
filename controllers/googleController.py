import os
import sys
import requests

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(parent, '.env'))
GCP_API_KEY = os.getenv('GCP_API_KEY')

class GoogleController:
    @staticmethod
    def getDistanceMatrix(origin_coords: str, dest_coords: str):
        params = {
            'origins': origin_coords,
            'destinations': dest_coords,
            'departure_time': 'now',
            'mode': 'driving',
            'traffic_model': 'pessimistic',
            'key': GCP_API_KEY
        }
        response = requests.get(url='https://maps.googleapis.com/maps/api/distancematrix/json', params=params)
        data = response.json()

        if data['rows'][0]['elements'][0]['status'] != 'OK':
            data['error'] = 'Invalid coordinates.'

        distance = data['rows'][0]['elements'][0]['distance']['value']
        elif distance < 500 or 1500 < distance:
            data['error'] = 'Distance must be between 500 to 1500 meters.'

        return data
