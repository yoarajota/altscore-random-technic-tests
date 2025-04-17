import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")

URL = os.getenv("URL")

class Client:
    def __init__(self):
        self.headers = {
            'API-KEY': API_KEY,
            'Content-Type': 'application/json',
        }

    def get_api_key(self):
        return self.api_key
    
    def get_request(self, endpoint, params=None):
        response = requests.get(
            URL + endpoint,
            params=params,
            headers=self.headers,
        )

        return response

    def post_request(self, endpoint, data=None, cookies=None):
        response = requests.post(
            URL + endpoint,
            headers=self.headers,
            json=data,
            cookies=cookies,
        )

        return response