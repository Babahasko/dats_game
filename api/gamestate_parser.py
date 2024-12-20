class GameState:
    def __init__(self, data):
        """
        Инициализация парсера с URL API.
        :param api_url: URL для запроса данных.
        """
        self.map_size =data.get("mapSize")
        self.name =data.get("name")
        self.points =data.get("points")
        self.fences =data.get("fences")
        self.snakes =data.get("snakes")
        self.enemies =data.get("enemies")
        self.food =data.get("food")
        self.special_food =data.get("specialFood")
        self.turn =data.get("turn")
        self.tick_remain_ms =data.get("tickRemainMs")
        self.revive_timeout_sec =data.get("reviveTimeoutSec")
        self.errors =data.get("errors")