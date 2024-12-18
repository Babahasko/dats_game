from utils import settings
import requests

class GameAPI:
    def __init__(self, api_key=settings.api.api_key, base_url=settings.api.server_url):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def get_map(self):
        """Получить карту поля боя."""
        url = f"{self.base_url}/api/map"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def scan(self):
        """Сканировать вокруг своих кораблей."""
        url = f"{self.base_url}/api/scan"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def ship_command(self, commands):
        """Отправить команды для управления юнитами"""
        url = f"{self.base_url}/api/shipCommand"
        payload = {"ships": commands}
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def register_death_match(self):
        """Регистрация на death match."""
        url = f"{self.base_url}/api/deathMatch/registration"
        response = requests.post(url, headers=self.headers)
        return response.json()

    def exit_death_match(self):
        """Выход из death match."""
        url = f"{self.base_url}/api/deathMatch/exitBattle"
        response = requests.post(url, headers=self.headers)
        return response.json()