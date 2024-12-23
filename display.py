import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import time
import threading
import asyncio

from utils import create_data_for_visualize
from utils import generate_fake_data

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

game_data = {
    'snakes': [],
    'fences': [],
    'food': [],
    'enemies': [],
    'special_food': []
}

# Callback для обновления состояния игры
@app.callback(Output('3d-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_game_state(n_intervals):
    figure = create_data_for_visualize( game_data['snakes'],
        game_data['fences'],
        game_data['food'],
        game_data['enemies'],
        game_data['special_food'])
    return figure

def run_dash_app():
    app.run_server(debug=False, use_reloader=False)

# Основной цикл работы змейки
async def main():
    in_game = True
    while in_game:
        try:
            # 1. Отправить первичный запрос на получение информации о своих змейках
            await asyncio.sleep(0.1)
            fake_data = generate_fake_data()
            game_data = fake_data

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