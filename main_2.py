import asyncio
import time
import threading
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from api import GameAPI, GameState
from logic import get_directions_for_snakes
from utils import create_data_for_visualize

game_api = GameAPI()
# Создаем приложение Dash
app = dash.Dash(__name__)

# Макет приложения
app.layout = html.Div([
    dcc.Graph(id='3d-graph', style={'height': '100vh'}),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Обновление каждую секунду
        n_intervals=0
    )
])

# Callback для обновления состояния игры
@app.callback(Output('3d-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_game_state(n_intervals, snakes, fences, food, enemies, special_food):
    figure = create_data_for_visualize(snakes, fences, food, enemies, special_food)
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