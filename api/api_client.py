# api/api_client.py

import requests
from config.config import API_KEYS, API_URL

class APIClient:
    def __init__(self):
        self.api_keys = API_KEYS
        self.api_url = API_URL
        self.current_key_index = 0

    def get_current_api_key(self):
        return self.api_keys[self.current_key_index]

    def switch_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)

    def send_request(self, data):
        headers = {
            "Authorization": f"Bearer {self.get_current_api_key()}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.api_url, json=data, headers=headers)
        if response.status_code != 200:
            self.switch_key()
        return response.json()
