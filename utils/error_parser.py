import json
from datetime import datetime
import pytz

def convert_to_local_time(utc_time_str, timezone='Europe/Moscow'):  # Замените на ваш часовой пояс
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
    local_time = utc_time.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(timezone))
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

def get_error_and_parse(json_string):
    data = json.loads(json_string)
    # Извлечь текущее время
    current_time_utc = data['error'].split("current time: ")[1].split(" next rounds:")[0].strip()
    current_time_local = convert_to_local_time(current_time_utc)
    print(f"Текущее время (ваш часовой пояс): {current_time_local}")

    # Извлечь раунды
    rounds_str = data['error'].split("next rounds: ")[1].strip()
    rounds = rounds_str.split("] [")

    for round_info in rounds:
        round_info = round_info.strip("[]")
        parts = round_info.split()
        round_name = parts[0]
        start_time_utc = parts[1].split("-")[0]
        end_time_utc = parts[2]

        # Преобразовать время
        start_time_local = convert_to_local_time(start_time_utc)
        end_time_local = convert_to_local_time(end_time_utc)

        return  f"Раунд: {round_name}, Начало: {start_time_local}, Конец: {end_time_local}"
