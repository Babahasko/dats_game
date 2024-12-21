import asyncio
import websockets
import random


async def send_data(websocket, path):
    while True:
        # Генерируем случайные 3D-точки
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        z = random.uniform(-10, 10)
        point = f"{x},{y},{z}"

        # Отправляем данные клиенту
        await websocket.send(point)
        await asyncio.sleep(0.1)  # Задержка 100 мс


# Создаем и запускаем сервер
async def main():
    async with websockets.serve(send_data, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Это предотвращает завершение цикла событий


# Запускаем сервер
asyncio.run(main())