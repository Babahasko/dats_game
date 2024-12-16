def generate_commands(scan_result):
    """Генерация команд для управления"""
    commands = []
    for ship in scan_result["scan"]["myShips"]:
        # Пример: каждый корабль движется вперед со скоростью 1
        commands.append({
            "ship_id": ship["id"],
            "speed": 1,
            "direction": ship["direction"]
        })
    return commands