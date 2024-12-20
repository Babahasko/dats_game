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

import heapq
import math


# Класс для представления узла в трехмерном пространстве
class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __lt__(self, other):
        return False  # Для работы с heapq


# Функция для вычисления эвристики (евклидово расстояние)
def heuristic(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


# Алгоритм A* для поиска пути в трехмерном пространстве
def a_star(start, goal, grid):
    # Преобразуем списки в объекты Node
    start_node = Node(*start)
    goal_node = Node(*goal)

    # Очередь с приоритетом
    open_set = []
    heapq.heappush(open_set, (0, start_node))

    # Словарь для хранения стоимости пути до каждого узла
    g_score = {start_node: 0}

    # Словарь для хранения оценки f(n) для каждого узла
    f_score = {start_node: heuristic(start_node, goal_node)}

    # Словарь для хранения предыдущих узлов (для восстановления пути)
    came_from = {}

    while open_set:
        # Извлекаем узел с наименьшим f(n)
        current = heapq.heappop(open_set)[1]

        # Если достигли цели
        if current == goal_node:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_node)
            return path[::-1]  # Возвращаем путь в правильном порядке

        # Проверяем соседей
        for dx, dy, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            neighbor = Node(current.x + dx, current.y + dy, current.z + dz)

            # Проверяем, что сосед находится в пределах сетки и не занят
            if (0 <= neighbor.x < len(grid) and
                    0 <= neighbor.y < len(grid[0]) and
                    0 <= neighbor.z < len(grid[0][0]) and
                    grid[neighbor.x][neighbor.y][neighbor.z] == 0):

                # Вычисляем стоимость пути до соседа
                tentative_g_score = g_score[current] + 1

                # Если найден лучший путь к соседу
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal_node)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # Если путь не найден
    return None


# Пример использования
if __name__ == "__main__":
    # Создаем трехмерную сетку (0 - свободно, 1 - занято)
    grid = [
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ],
        [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ],
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
    ]

    # Начальная позиция змейки (в виде списка)
    start_position = [0, 0, 0]

    # Позиция еды (в виде списка)
    goal_position = [2, 2, 2]

    # Находим путь
    path = a_star(start_position, goal_position, grid)

    if path:
        print("Путь найден:")
        for node in path:
            print(f"({node.x}, {node.y}, {node.z})")
    else:
        print("Путь не найден")