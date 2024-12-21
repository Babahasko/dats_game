import plotly.graph_objs as go
from utils import logger
import itertools

def create_data_for_visualize(snakes): # fences, food, enemies, special_food
    data = []
    # Рисуем змеек
    for snake in snakes:
        if snake['status'] == "alive":
            x = [point[0] for point in snake['geometry']]
            y = [point[1] for point in snake['geometry']]
            z = [point[2] for point in snake['geometry']]
            data.append(go.Scatter3d(
                x=x, y=y, z=z,
                mode='markers',
                name=f"Snake {snake['id']}",
                marker=dict(
                    size = 5,
                    color='green')
            ))

    # # Рисуем препятствия
    # x = [fence[0] for fence in fences]
    # y = [fence[1] for fence in fences]
    # z = [fence[2] for fence in fences]
    # data.append(go.Scatter3d(x=x, y=y, z=z, mode='markers', name='Fences', marker=dict(size=5, color='red')))
    #
    # # Рисуем еду
    # for f in food:
    #     x, y, z = f['c']
    #     data.append(go.Scatter3d(x=[x], y=[y], z=[z], mode='markers', name='Food', marker=dict(size=5, color='green')))
    #
    # # Рисуем врагов
    # for enemy in enemies:
    #     x, y, z = zip(*enemy['geometry'])
    #     data.append(go.Scatter3d(x=x, y=y, z=z, mode='lines+markers', name=f"Enemy {enemy['status']}"))

    # Рисуем специальную еду
    # for sf in special_food['golden']:
    #     x, y, z = sf
    #     data.append(
    #         go.Scatter3d(x=[x], y=[y], z=[z], mode='markers', name='Special Food', marker=dict(size=5, color='yellow')))


    return data

def create_data_for_visualize_2(snakes, fences):
    data = []
    # Рисуем змеек
    cube_size = 1
    for snake in snakes:
        if snake['status'] == "alive":
            x = [point[0] for point in snake['geometry']]
            y = [point[1] for point in snake['geometry']]
            z = [point[2] for point in snake['geometry']]
            for xi, yi, zi in zip(x, y, z):
                cube = create_cube(xi,yi,zi,cube_size,'green' )
                data.append(cube)
    # Рисуем препятствия
    x = [fence[0] for fence in fences]
    y = [fence[1] for fence in fences]
    z = [fence[2] for fence in fences]
    for xi, yi, zi in zip(x, y, z):
        cube = create_cube(xi, yi, zi, cube_size, 'blue')
        data.append(cube)
        # logger.info(f"add fence cube {cube}")
    # cubes = create_cube(x,y,z, color='blue')
    # logger.info(f"fence_cubes {cubes}")
    # data.append(cubes)
    return data


def create_cube(x, y, z, size, color):
    # Вершины куба
    vertices = [
        [x - size / 2, y - size / 2, z - size / 2],
        [x + size / 2, y - size / 2, z - size / 2],
        [x + size / 2, y + size / 2, z - size / 2],
        [x - size / 2, y + size / 2, z - size / 2],
        [x - size / 2, y - size / 2, z + size / 2],
        [x + size / 2, y - size / 2, z + size / 2],
        [x + size / 2, y + size / 2, z + size / 2],
        [x - size / 2, y + size / 2, z + size / 2]
    ]

    # Индексы граней куба
    faces = [
        [0, 1, 2, 3],  # Нижняя грань
        [4, 5, 6, 7],  # Верхняя грань
        [0, 1, 5, 4],  # Передняя грань
        [2, 3, 7, 6],  # Задняя грань
        [0, 3, 7, 4],  # Левая грань
        [1, 2, 6, 5]   # Правая грань
    ]

    # Создаем куб
    cube = go.Mesh3d(
        x=[v[0] for v in vertices],
        y=[v[1] for v in vertices],
        z=[v[2] for v in vertices],
        i=[f[0] for f in faces],
        j=[f[1] for f in faces],
        k=[f[2] for f in faces],
        color=color,
        opacity=1  # Полная непрозрачность
    )
    return cube


def convert_data_for_visual(game_state):
    snakes_geometry = [snake['geometry'] for snake in game_state.snakes]
    result_snakes = list(itertools.chain(*snakes_geometry))
    enemies_geometry = [enemie['geometry'] for enemie in game_state.enemies]
    result_enemies = list(itertools.chain(*enemies_geometry))
    food_c = [food['c'] for food in game_state.food]
    result = {
        "map_size": game_state.map_size,
        "food": food_c,
        "enemies": result_enemies,
        "snakes": result_snakes,
        "fences": game_state.fences,
    }
    return result