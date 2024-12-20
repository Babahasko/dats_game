from api import GameAPI, GameState
from display import display_game_state
from utils import logger
import asyncio

from logic import get_directions_for_snakes
import time

game_api = GameAPI()

#Основной цикл работы змейки
async def main():
    in_game = True
    while in_game:
        try:
            #1. Отправить первичный запрос на получение информации о своих змейках
            bold_direction = {"snakes": []}
            direction_response = await game_api.put_direction(payload = bold_direction)
            if isinstance(direction_response, dict):
                game_state = GameState(direction_response)
                directions = get_directions_for_snakes(game_state)
                give_direction = directions

                #2. Отправить запрос на передвижение
                await game_api.put_direction(payload = give_direction)

                # 3. Подождать оставшееся время до конца хода
                remaining_time = game_state.tick_remain_ms
                if remaining_time > 0:
                    print(f"Ожидание до конца хода: {remaining_time} секунд")
                    time.sleep(remaining_time/1000)
                else:
                    print("Время до конца хода не получено, ожидание 1 секунды")
                    time.sleep(1)
            else:
                print(direction_response)
                in_game = False

        except KeyboardInterrupt:
            print("Цикл остановлен пользователем.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(1)  # Пауза перед повторной попыткой

if __name__ == "__main__":
    asyncio.run(main())
