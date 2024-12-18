from utils import logger

def display_game_state(scan_result):
    """Отображение текущего состояния игры."""
    logger.info(f"Тик: {scan_result['scan']['tick']}")
    logger.info("Мои корабли:")
    for ship in scan_result["scan"]["myShips"]:
        logger.info(f"ID: {ship['id']}, Позиция: {ship['position']}, Здоровье: {ship['health']}")
    logger.info("Вражеские корабли:")
    for ship in scan_result["scan"]["enemyShips"]:
        logger.info(f"Позиция: {ship['position']}, Здоровье: {ship['health']}")
    logger.info("Зона сужения:", scan_result["scan"]["zone"])
    logger.info("-" * 40)