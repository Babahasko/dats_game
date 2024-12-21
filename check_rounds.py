import asyncio
import websockets
import asyncio
import time
import threading
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import json

from api import GameAPI, GameState
from logic import get_directions_for_snakes
from utils import create_data_for_visualize, create_data_for_visualize_2
from utils import logger
from utils import get_error_and_parse, convert_data_for_visual

game_api = GameAPI()

# Словарь для хранения подключенных клиентов
connected_clients = set()

async def send_game_state(visual_data):
    """
    Отправляет game_state всем подключенным клиентам через WebSocket.
    """
    if connected_clients:
        for client in connected_clients:
            await client.send(visual_data)

async def websocket_server(websocket):
    """
    Обрабатывает подключения клиентов.
    """
    # Добавляем клиента в список подключенных
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Здесь можно обрабатывать сообщения от клиента, если нужно
            pass
    finally:
        # Удаляем клиента при отключении
        connected_clients.remove(websocket)


async def main():
    # Запускаем WebSocket-сервер
    server = await websockets.serve(websocket_server, "localhost", 8765)

    in_game = True
    while in_game:
        try:
            # 1. Отправить первичный запрос на получение информации о своих змейках
            bold_direction = {"snakes": []}
            direction_response = await game_api.put_direction(payload=bold_direction)
            if isinstance(direction_response, dict):
                game_state = GameState(direction_response)
                directions = get_directions_for_snakes(game_state)
                give_direction = directions

                # 2. Отправить запрос на передвижение
                await game_api.put_direction(payload=give_direction)

                #Преобразование game_state
                visual_data = convert_data_for_visual(game_state)
                json_visual_data = json.dumps(visual_data)

                # 3. Отправить game_state через WebSocket
                await send_game_state(json_visual_data)

                # 4. Подождать оставшееся время до конца хода
                remaining_time = game_state.tick_remain_ms
                if remaining_time > 0:
                    print(f"Ожидание до конца хода: {remaining_time} милисекунд")
                    await asyncio.sleep(remaining_time / 1000)
                else:
                    print("Время до конца хода не получено, ожидание 1 секунды")
                    await asyncio.sleep(1)
            else:
                in_game = False
                print(direction_response)

        except KeyboardInterrupt:
            print("Цикл остановлен пользователем.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            await asyncio.sleep(1)  # Пауза перед повторной попыткой

    # Останавливаем WebSocket-сервер
    server.close()
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())