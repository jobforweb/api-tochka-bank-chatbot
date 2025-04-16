# api/api_client.py

import aiohttp
from config.config import BASE_URL, HEADERS


class TochkaAPIClient:
    async def get_balances(self):
        """
        Получает данные о балансах через API.
        :return: JSON-ответ от сервера.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(BASE_URL, headers=HEADERS) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                print(f"Ошибка при запросе к API: {e}")
                return None