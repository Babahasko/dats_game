import asyncio
import time
import threading
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from api import GameAPI, GameState
from logic import get_directions_for_snakes
from utils import create_data_for_visualize, create_data_for_visualize_2
from utils import logger
from utils import get_error_and_parse

game_api = GameAPI()


# Основной цикл работы змейки
async def main():
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

                # 3. Подождать оставшееся время до конца хода
                remaining_time = game_state.tick_remain_ms
                if remaining_time > 0:
                    print(f"Ожидание до конца хода: {remaining_time} милисекунд")
                    time.sleep(remaining_time / 1000)
                else:
                    print("Время до конца хода не получено, ожидание 1 секунды")
                    time.sleep(1)
            else:
                in_game = False
                print(direction_response)
                readable_response = get_error_and_parse(direction_response)
                print(readable_response)


        except KeyboardInterrupt:
            print("Цикл остановлен пользователем.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(1)  # Пауза перед повторной попыткой

if __name__ == "__main__":
    # Запускаем основной цикл игры
    asyncio.run(main())