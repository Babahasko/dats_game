from utils import logger

import math


def find_nearest_food(snake_position, food_list):
    """
    Находит координаты ближайшей еды из списка.

    :param snake_position: Координаты змейки в виде списка [x, y, z].
    :param food_list: Список координат еды в виде списка списков [[x1, y1, z1], [x2, y2, z2], ...].
    :return: Координаты ближайшей еды в виде списка [x, y, z].
    """
    if not food_list:
        return None  # Если список еды пуст, возвращаем None

    # Инициализируем минимальное расстояние и ближайшую еду
    min_distance = float('inf')
    nearest_food = None

    # Проходим по всем координатам еды
    for food in food_list:
        # Вычисляем евклидово расстояние между змейкой и едой
        distance = math.sqrt(
            (snake_position[0] - food[0]) ** 2 +
            (snake_position[1] - food[1]) ** 2 +
            (snake_position[2] - food[2]) ** 2
        )

        # Если текущее расстояние меньше минимального, обновляем минимальное расстояние и ближайшую еду
        if distance < min_distance:
            min_distance = distance
            nearest_food = food

    return nearest_food

def get_directions_for_snakes(game_state):
    moves = {"snakes": []}
    try:
        for index, snake in enumerate(game_state.snakes):
            snake_position = game_state.snakes[index]['geometry']
            snake_position = snake_position[0]
            # logger.info(game_state.snakes)
            food_position = game_state.food[0]['c']

            # Находим ближайшую еду
            # logger.debug(game_state.food)
            result = [item['c'] for item in game_state.food]
            # logger.info(result)
            nearest_food = find_nearest_food(snake_position, result)

            # Выводим результат
            # print("Ближайшая еда:", nearest_food)
            # logger.info(nearest_food)

            fences = game_state.fences
            players = game_state.enemies
            # direction = choose_direction(snake_position, food_position, fences, players)
            direction = choose_direction(snake_position, nearest_food, fences, players)

            moves["snakes"].append({
                "id": snake['id'],
                "direction": [direction['x'], direction['y'], direction['z']]
            })
    except Exception as e:
        pass
        # logger.error(e)
        print(e)
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
        'x': food_position[0] - snake_position[0],
        'y': food_position[1] - snake_position[1],
        'z': food_position[2] - snake_position[2]
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
            'x': snake_position[0] + direction['x'],
            'y': snake_position[1] + direction['y'],
            'z': snake_position[2] + direction['z']
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