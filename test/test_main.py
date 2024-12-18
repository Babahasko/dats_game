# from unittest.mock import patch
# import pytest
#
# from api import GameAPI
# from utils import settings
#
#
# import pytest
# from unittest.mock import MagicMock
# from main import main
#
# @pytest.fixture
# def mock_api(mocker):
#     api = MagicMock()
#     mocker.patch('main.GameAPI', return_value=api)
#     return api
#
# def test_main_successful_registration(mock_api, capsys, mocker):
#     # Настройка моков
#     mock_api.register_death_match.return_value = {"success": True}
#     mock_api.scan.return_value = {"success": True, "scan": {
#         "tick": 1,
#         "myShips": [{"id": 1, "position": (0, 0), "health": 100, "direction": "N"}],
#         "enemyShips": [{"position": (1, 1), "health": 50}],
#         "zone": {"radius": 100, "center": (0, 0)}
#     }}
#     mock_api.ship_command.return_value = {"success": True}
#
#     # Моки для display_game_state и generate_commands
#     mocker.patch('main.display_game_state')
#     mocker.patch('main.generate_commands', return_value=[{"ship_id": 1, "speed": 1, "direction": "N"}])
#
#     # Запуск main
#     main()
#
#     # Проверка вызовов
#     mock_api.register_death_match.assert_called_once()
#     mock_api.scan.assert_called_once()
#     mock_api.ship_command.assert_called_once()
#     mock_api.exit_death_match.assert_called_once()
#
#
#
