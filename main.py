from api import GameAPI, GameState
from display import display_game_state
from utils import logger
import asyncio

from logic import get_directions_for_snakes
import time

game_api = GameAPI()

#Основной цикл работы змейки
async def main():
    #отправить первичный запрос на получение информации о своих змейках
    bold_direction = {"snakes": []}
    direction_response = await game_api.put_direction(payload = bold_direction)
    logger.info(direction_response)
    if isinstance(direction_response, dict):
        game_state = GameState(direction_response)
        directions = get_directions_for_snakes(game_state)
        logger.info(f"{directions}")
    #Получение раундов
    # game_rounds = await game_api.get_game_rounds()

    #подождать оставшееся время до конца хода

if __name__ == "__main__":
    asyncio.run(main())
