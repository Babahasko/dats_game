import pytest
from unittest.mock import patch, MagicMock

from utils import settings
from api import GameAPI


@pytest.fixture
def game_api():
    return GameAPI(api_key=settings.api.api_key, base_url=settings.api.server_url)

@patch('requests.get')
def test_get_map(mock_get, game_api):
    # Подготовка мока
    mock_response = MagicMock()
    mock_response.json.return_value = {"map": "battlefield"}
    mock_get.return_value = mock_response

    # Вызов тестируемой функции
    result = game_api.get_map()

    # Проверка результата
    assert result == {"map": "battlefield"}
    mock_get.assert_called_once_with(f"{settings.api.server_url}/api/map", headers=game_api.headers)

@patch('requests.get')
def test_scan(mock_get, game_api):
    # Подготовка мока
    mock_response = MagicMock()
    mock_response.json.return_value = {"scan": "results"}
    mock_get.return_value = mock_response

    # Вызов тестируемой функции
    result = game_api.scan()

    # Проверка результата
    assert result == {"scan": "results"}
    mock_get.assert_called_once_with(f"{settings.api.server_url}/api/scan", headers=game_api.headers)

@patch('requests.post')
def test_ship_command(mock_post, game_api):
    # Подготовка мока
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success"}
    mock_post.return_value = mock_response

    # Вызов тестируемой функции
    commands = [{"id": 1, "command": "move"}]
    result = game_api.ship_command(commands)

    # Проверка результата
    assert result == {"status": "success"}
    mock_post.assert_called_once_with(
        f"{settings.api.server_url}/api/shipCommand",
        headers=game_api.headers,
        json={"ships": commands}
    )

@patch('requests.post')
def test_register_death_match(mock_post, game_api):
    # Подготовка мока
    mock_response = MagicMock()
    mock_response.json.return_value = {"registration": "success"}
    mock_post.return_value = mock_response

    # Вызов тестируемой функции
    result = game_api.register_death_match()

    # Проверка результата
    assert result == {"registration": "success"}
    mock_post.assert_called_once_with(
        f"{settings.api.server_url}/api/deathMatch/registration",
        headers=game_api.headers
    )

@patch('requests.post')
def test_exit_death_match(mock_post, game_api):
    # Подготовка мока
    mock_response = MagicMock()
    mock_response.json.return_value = {"exit": "success"}
    mock_post.return_value = mock_response

    # Вызов тестируемой функции
    result = game_api.exit_death_match()

    # Проверка результата
    assert result == {"exit": "success"}
    mock_post.assert_called_once_with(
        f"{settings.api.server_url}/api/deathMatch/exitBattle",
        headers=game_api.headers
    )