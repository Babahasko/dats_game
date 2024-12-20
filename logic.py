# def generate_commands(scan_result):
#     """Генерация команд для управления"""
#     commands = []
#     for ship in scan_result["scan"]["myShips"]:
#         # Пример: каждый корабль движется вперед со скоростью 1
#         commands.append({
#             "ship_id": ship["id"],
#             "speed": 1,
#             "direction": ship["direction"]
#         })
#     return commands

import time

def get_directions_for_snakes(game_state):
    moves = {"snakes": []}
    for snake in game_state.snakes:
        snake_position = game_state.snakes
        food_position = game_state.food
        fences = game_state.fences
        players = game_state.enemies
        direction = choose_direction(snake_position, food_position, fences, players)
        moves["snakes"].append({
            "id": snake.id,
            "direction": [direction['x'], direction['y'], direction['z']]
        })
    return moves

# Функция для получения текущего состояния игры
def get_game_state():
    pass
#     response = requests.get(f"{BASE_URL}/game/state")
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print("Ошибка при получении состояния игры")
#         return None
#

# Функция для отправки направлений движения всех змеек
def send_moves(moves):
    pass
    # response = requests.post(f"{BASE_URL}/game/move", json=moves)
    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     print("Ошибка при отправке направлений движения")
    #     return None


# Функция для выбора направления движения для одной змейки
def choose_direction(snake_position, food_position, fences, players):
    # Вычисляем направление к еде
    direction_to_food = {
        'x': food_position['x'] - snake_position['x'],
        'y': food_position['y'] - snake_position['y'],
        'z': food_position['z'] - snake_position['z']
    }

    # Определяем возможные направления движения
    possible_directions = [
        {'x': 1, 'y': 0, 'z': 0},
        {'x': -1, 'y': 0, 'z': 0},
        {'x': 0, 'y': 1, 'z': 0},
        {'x': 0, 'y': -1, 'z': 0},
        {'x': 0, 'y': 0, 'z': 1},
        {'x': 0, 'y': 0, 'z': -1}
    ]

    # Фильтруем направления, которые приведут к столкновению с препятствиями или другими игроками
    safe_directions = []
    for direction in possible_directions:
        new_position = {
            'x': snake_position['x'] + direction['x'],
            'y': snake_position['y'] + direction['y'],
            'z': snake_position['z'] + direction['z']
        }
        if new_position not in fences and new_position not in players:
            safe_directions.append(direction)

    # Выбираем направление, которое ближе всего к еде
    best_direction = None
    best_distance = float('inf')
    for direction in safe_directions:
        distance = abs(direction_to_food['x'] - direction['x']) + abs(direction_to_food['y'] - direction['y']) + abs(
            direction_to_food['z'] - direction['z'])
        if distance < best_distance:
            best_distance = distance
            best_direction = direction

    return best_direction


# Основной цикл игры
def game_loop():
    pass
    # while True:
    #     # Получаем текущее состояние игры
    #     game_state = get_game_state()
    #
    #     if game_state is None:
    #         break
    #
    #     # Создаём список для хранения направлений всех змеек
    #     moves = {"snakes": []}
    #
    #     # Обрабатываем каждую змейку
    #     for snake_id in SNAKE_IDS:
    #         # Находим данные текущей змейки
    #         snake = next((s for s in game_state['snakes'] if s['id'] == snake_id), None)
    #         # if snake is None:
    #         #     print(f"Змейка с ID {snake_id} не найдена в состоянии игры")
    #         #     continue
    #
    #         # Получаем положение змейки, еды, препятствий и других игроков
    #         snake_position = game_state.snakes
    #         food_position = game_state.food
    #         fences = game_state.fences
    #         players = game_state.enemies
    #
    #         # Выбираем направление движения для текущей змейки
    #         direction = choose_direction(snake_position, food_position, fences, players)
    #
    #         if direction is None:
    #             print(f"Нет безопасных направлений для движения змейки {snake_id}")
    #             continue
    #
    #         # Добавляем направление в список
    #         moves["snakes"].append({
    #             "id": snake_id,
    #             "direction": [direction['x'], direction['y'], direction['z']]
    #         })
    #
    #     # Отправляем направления движения всех змеек
    #     response = send_moves(moves)
    #
    #     if response is None:
    #         break
    #
    #     # Пауза для следующего хода
    #     time.sleep(1)


# Запуск игры
# game_loop()