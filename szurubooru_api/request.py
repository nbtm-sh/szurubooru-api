import szurubooru_api.auth
import requests

class Request:
    def __init__(self, username, api_token, user_agent="szurubooru-api (github: nbtm-sh/szurubooru-api)"):
        self.token = szurubooru_api.auth.generate_auth_token(username, api_token)

    def get(self, url):
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return requests.get(url, headers=headers)

    def post(self, url, data=None, files=None):
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return requests.post(url, headers=headers, data=data, files=files)

    def put(self, data=None):
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return requests.put(url, headers=headers, data=data)

    def delete(self, data=None):
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return requests.delete(url, headers=headers, data=data)
