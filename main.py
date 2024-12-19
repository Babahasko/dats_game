from api import GameAPI
from logic import generate_commands
from display import display_game_state
from utils import logger

import time

api = GameAPI()

def main():
    # Пытаемся зарегаться
    logger.info('Запуск бота')
    try:
        registration_result = api.register_death_match()
        if not registration_result.get("success"):
            logger.info(f"Ошибка регистрации")
            # logger.info(f"Ошибка регистрации:, {registration_result.get("errors")}")
    except Exception as e:
        logger.info(f"Ошибка регистрации")

    logger.info(f"Регистрация успешна!")

    in_game=True

    while in_game:
        try:
            # Получение данных о текущем состоянии игры
            scan_result = api.scan()
            if not scan_result.get("success"):
                logger.info(f"Ошибка сканирования:, {scan_result.get('errors')}")
                break

            # Отображение данных
            display_game_state(scan_result)

            # Логика управления флотом
            commands = generate_commands(scan_result)

            # Отправка команд
            command_result = api.ship_command(commands)
            if not command_result.get("success"):
                logger.info(f"Ошибка отправки команд:, {command_result.get("errors")}")
                break

            # Ожидание следующего тика
            time.sleep(1)
            in_game=False

        except KeyboardInterrupt:
            logger.info(f"Выход из игры...")
            break

    api.exit_death_match()

if __name__ == "__main__":
    main()