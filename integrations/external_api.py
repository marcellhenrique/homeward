import requests

class ExternalAPIService:
    BASE_URL = "https://api.homeward.com"

    @staticmethod
    def fetch_applications():
        url = f"{ExternalAPIService.BASE_URL}/applications/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def fetch_customers():
        url = f"{ExternalAPIService.BASE_URL}/customers/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
