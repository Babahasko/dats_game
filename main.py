from api import GameAPI, GameState
from display import display_game_state
from utils import logger
import asyncio

import time

game_api = GameAPI()

#Основной цикл работы змейки
async def main():
    #отправить первичный запрос на получение информации о своих змейках
    bold_direction = {"snakes": []}
    direction_response = await game_api.put_direction(payload = bold_direction)
    logger.info(f"{direction_response}")
    game_state = GameState(direction_response)
    logger.info(f"game_state.snakes = {game_state.snakes}")
    logger.info(f"{game_state.snakes}")

    #Получение раундов
    # game_rounds = await game_api.get_game_rounds()

    #отправить запрос на команду о передвижении

    #подождать оставшееся время до конца хода


if __name__ == "__main__":
    asyncio.run(main())
