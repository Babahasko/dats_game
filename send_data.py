import asyncio
import websockets
import json
import random


# Функция для генерации случайного JSON
def generate_random_json():
    return {
        "id": random.randint(1, 100),
        "name": "Item" + str(random.randint(1, 10)),
        "value": round(random.uniform(0, 100), 2),
        "isActive": random.choice([True, False])
    }


# Обработчик WebSocket
async def send_json(websocket):
    while True:
        # Генерируем случайный JSON
        random_json = generate_random_json()

        # Преобразуем JSON в строку
        json_data = json.dumps(random_json)

        # Отправляем JSON клиенту
        await websocket.send(json_data)

        # Ждем 1 секунду перед отправкой следующего сообщения
        await asyncio.sleep(1)


# Запуск сервера
async def main():
    async with websockets.serve(send_json, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Бесконечный цикл


# Запускаем сервер
asyncio.run(main())