def display_game_state(scan_result):
    """Отображение текущего состояния игры."""
    print(f"Тик: {scan_result['scan']['tick']}")
    print("Мои корабли:")
    for ship in scan_result["scan"]["myShips"]:
        print(f"ID: {ship['id']}, Позиция: {ship['position']}, Здоровье: {ship['health']}")
    print("Вражеские корабли:")
    for ship in scan_result["scan"]["enemyShips"]:
        print(f"Позиция: {ship['position']}, Здоровье: {ship['health']}")
    print("Зона сужения:", scan_result["scan"]["zone"])
    print("-" * 40)