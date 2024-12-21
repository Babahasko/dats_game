import asyncio
import time
import threading
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from api import GameAPI, GameState
from logic import get_directions_for_snakes
from utils import create_data_for_visualize, create_data_for_visualize_2
from utils import logger
from utils import get_error_and_parse

game_api = GameAPI()


map_size = [300, 300, 90]
snakes = []
fences = []


# Создаем приложение Dash
app = dash.Dash(__name__)
# Макет приложения
app.layout = html.Div([
    dcc.Graph(id='3d-graph', style={'height': '100vh'}),
    dcc.Store(id='data-store'),
    dcc.Store(id='camera-state-store'),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Обновление каждую секунду
        n_intervals=0
    )
])

# Колбэк для сохранения состояния камеры
@app.callback(
    Output('camera-state-store', 'data'),  # Сохраняем состояние камеры в dcc.Store
    Input('3d-graph', 'relayoutData')  # Триггер: изменение relayoutData
)
def save_camera_state(relayout_data):
    # Проверяем, содержит ли relayoutData информацию о камере
    if relayout_data and 'scene.camera' in relayout_data:
        logger.info(f"Saving camera state: {relayout_data['scene.camera']}")
        return relayout_data['scene.camera']  # Возвращаем состояние камеры
    return dash.no_update  # Если данных о камере нет, ничего не обновляем

#Коллбэк для обновления состояния игры
@app.callback(
    Output('data-store', 'data'),
    Input('interval-component', 'n_intervals')  # Триггер обновления
)
def update_global_data(n_intervals):
    global snakes, map_size
    data = [map_size, snakes, fences]
    return data

# Callback для обновления графика
@app.callback(
    Output('3d-graph', 'figure'),
    Input('data-store', 'data'),
    State('camera-state-store', 'data')
)

def update_game_state(data, camera_state):
    map_size = data[0]
    snakes = data[1]
    fences = data[2]
    data = create_data_for_visualize_2(snakes, fences)
    figure = go.Figure(data=data)
    figure.update_layout(
        title="3D Visualization of Snakes",
        scene=dict(
            xaxis=dict(range=[0, map_size[0]], title='X'),
            yaxis=dict(range=[0, map_size[1]], title='Y'),
            zaxis=dict(range=[0, map_size[2]], title='Z'),
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=1)  # Пропорции осей
        ),
        showlegend=True
    )
    if camera_state:
        logger.info(f"Applying camera state: {camera_state}")
        figure.update_layout(scene_camera=camera_state)
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

                # Сохранение данных для графика
                global map_size
                map_size = game_state.map_size
                global snakes
                snakes = game_state.snakes
                global fences
                fences = game_state.fences

                directions = get_directions_for_snakes(game_state)
                logger.info(directions)
                give_direction = directions

                # 2. Отправить запрос на передвижение
                await game_api.put_direction(payload=give_direction)

                # 3. Подождать оставшееся время до конца хода
                remaining_time = game_state.tick_remain_ms
                if remaining_time > 0:
                    print(f"Ожидание до конца хода: {remaining_time} милисекунд")
                    time.sleep(remaining_time / 1000)
                else:
                    print("Время до конца хода не получено, ожидание 1 секунды")
                    time.sleep(1)
            else:
                in_game = False
                print(direction_response)
                readable_response = get_error_and_parse(direction_response)
                print(readable_response)


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