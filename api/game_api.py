import json

from utils import settings
import aiohttp
import asyncio

class GameAPI:
    def __init__(self, api_key=settings.api.api_key, base_url=settings.api.server_url):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "X-Auth-Token": self.api_key,
            "Content-Type": "application/json"
        }

    async def put_direction(self, payload):
        """Выбрать направление змейки"""
        url = f"{self.base_url}/play/snake3d/player/move"
        json_payload = json.dumps(payload)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, data=json_payload) as response:
                return await response.text()

    async def get_game_rounds(self):
        """Получить расписание раундов"""
        url = f"{self.base_url}/rounds/snake3d"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                return await response.text()