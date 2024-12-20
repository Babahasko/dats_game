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

# Функция для отправки направления движения змейки
def send_move(direction):
    pass

# Функция для выбора направления движения
def choose_direction(game_state):
    # Получаем текущее положение змейки
    snake_position = game_state.snakes

    # Получаем положение еды
    food_position = game_state.food

    # Получаем положение препятствий и других игроков
    obstacles = game_state.fences
    players = game_state.enemies

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
        if new_position not in obstacles and new_position not in players:
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
    while True:
        # Получаем текущее состояние игры
        game_state = GameState(response)

        if game_state is None:
            break

        # Выбираем направление движения
        direction = choose_direction(game_state)

        if direction is None:
            print("Нет безопасных направлений для движения")
            break

        # Отправляем направление движения
        response = send_move(direction)

        if response is None:
            break

        # Пауза для следующего хода
        time.sleep(1)


# Запуск игры
# game_loop()