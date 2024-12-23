import asyncio
import time
import threading
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from api import GameAPI, GameState
from logic import get_directions_for_snakes
from utils import create_data_for_visualize
from utils import logger
game_api = GameAPI()


map_size = [300, 300, 90]
snakes = []


# Создаем приложение Dash
app = dash.Dash(__name__)
# Макет приложения
app.layout = html.Div([
    dcc.Graph(id='3d-graph', style={'height': '100vh'}),
    dcc.Store(id='data-store'),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Обновление каждую секунду
        n_intervals=0
    )
])

#Коллбэк для обновления состояния игры
@app.callback(
    Output('data-store', 'data'),
    Input('interval-component', 'n_intervals')  # Триггер обновления
)
def update_global_data(n_intervals):
    global snakes, map_size
    data = [map_size, snakes]
    return data

# Callback для обновления графика
@app.callback(
    Output('3d-graph', 'figure'),
    Input('data-store', 'data')
)

def update_game_state(data):
    map_size = data[0]
    snakes = data[1]
    data = create_data_for_visualize(map_size, snakes)
    figure = go.Figure(data=data)
    figure.update_layout(
        title="3D Visualization of Snakes",
        scene=dict(
            xaxis=dict(range=[0, map_size[0]], title='X'),
            yaxis=dict(range=[0, map_size[1]], title='Y'),
            zaxis=dict(range=[0, map_size[2]], title='Z'),
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=0.3)  # Пропорции осей
        ),
        showlegend=True
    )
    return figure

# Функция для запуска Dash в отдельном потоке
def run_dash_app():
    app.run_server(debug=False, use_reloader=False)

# Основной цикл работы змейки
async def main():
    in_game = True
    while in_game:
        try:
            # 1. Отправить первичный запрос на получение информации о своих змейках
            bold_direction = {"snakes": []}
            direction_response = await game_api.put_direction(payload=bold_direction)
            if isinstance(direction_response, dict):
                game_state = GameState(direction_response)
                global map_size
                map_size = game_state.map_size
                global snakes
                snakes = game_state.snakes
                # fences = game_state.fences
                # enemies = game_state.enemies
                # special_food = game_state.special_food
                directions = get_directions_for_snakes(game_state)
                give_direction = directions

                # 2. Отправить запрос на передвижение
                await game_api.put_direction(payload=give_direction)

                # 3. Подождать оставшееся время до конца хода
                remaining_time = game_state.tick_remain_ms
                if remaining_time > 0:
                    print(f"Ожидание до конца хода: {remaining_time} секунд")
                    time.sleep(remaining_time / 1000)
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
    # Запускаем Dash в отдельном потоке
    dash_thread = threading.Thread(target=run_dash_app)
    dash_thread.daemon = True  # Поток завершится, когда завершится основной процесс
    dash_thread.start()

    # Запускаем основной цикл игры
    asyncio.run(main())