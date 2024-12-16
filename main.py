from game_api import GameAPI
from logic import generate_commands
from display import display_game_state
import time

api = GameAPI()

def main():
    registration_result = api.register_death_match()
    if not registration_result.get("success"):
        print("Ошибка регистрации:", registration_result.get("errors"))
        return

    print("Регистрация успешна!")

    while True:
        try:
            # Получение данных о текущем состоянии игры
            scan_result = api.scan()
            if not scan_result.get("success"):
                print("Ошибка сканирования:", scan_result.get("errors"))
                break

            # Отображение данных
            display_game_state(scan_result)

            # Логика управления флотом
            commands = generate_commands(scan_result)

            # Отправка команд
            command_result = api.ship_command(commands)
            if not command_result.get("success"):
                print("Ошибка отправки команд:", command_result.get("errors"))
                break

            # Ожидание следующего тика
            time.sleep(3)

        except KeyboardInterrupt:
            print("Выход из игры...")
            break

    api.exit_death_match()