# Структура

**logic.py** - функции для управления логикой бота

**config.py** - переменные, которые не меняются со временем

**disply.py** - функции по отображению карты

**main.py** - основная точка входа в приложение и запуск бота

**game_api** - интерфейс для взаимодействия с API

**test.py** - функции тестирования

# Установка виртуального окружения

```python
python -m venv .venv
python -m pip install --upgrade pip
```
Установка зависимостей

```python
pip install -r requirements.txt
```
# Начальная настройка проекта

Добавить в файл ".env.template"
```python
API_KEY = "<api_key>"
SERVER_URL = "<server_url>"
```
переименовать файл в ".env"

# Запуск бота

```python
python main.py
```

