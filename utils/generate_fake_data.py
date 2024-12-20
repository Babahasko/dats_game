import random
import string
import uuid

def generate_fake_data():
    def generate_snake():
        return {
            'id': uuid.uuid4().hex,
            'direction': [0, 0, 0],
            'oldDirection': [0, 0, 0],
            'geometry': [[random.randint(0, 200), random.randint(0, 200), random.randint(0, 50)]],
            'deathCount': 0,
            'status': 'alive',
            'reviveRemainMs': 0
        }

    def generate_fences(n):
        """
        Генерирует список из n элементов, где каждый элемент — это список из трех случайных чисел.

        :param n: Количество элементов в списке.
        :return: Список списков с тремя случайными числами.
        """
        fences = []
        for _ in range(n):
            fence = [
                random.randint(0, 168),  # Первое число от 0 до 168
                random.randint(0, 168),  # Второе число от 0 до 168
                random.randint(0, 58)  # Третье число от 0 до 58
            ]
            fences.append(fence)
        return fences

    def generate_food():
        return {
            'c': [random.randint(0, 200), random.randint(0, 200), random.randint(0, 50)],
            'points': random.randint(1, 20),
            'type': 0
        }

    def generate_enemy():
        return {
            'geometry': [[random.randint(0, 200), random.randint(0, 200), random.randint(0, 50)]],
            'status': 'alive',
            'kills': 0
        }

    def generate_special_food():
        return {
            'golden': [
                [random.randint(0, 200), random.randint(0, 200), random.randint(0, 50)],
                [random.randint(0, 200), random.randint(0, 200), random.randint(0, 50)]
            ]
        }

    snakes = [generate_snake() for _ in range(3)]
    fences = [generate_fences(10)]
    food = [generate_food() for _ in range(10)]
    enemies = [generate_enemy() for _ in range(2)]
    special_food = generate_special_food()

    return {
        'snakes': snakes,
        'fences': fences,
        'food': food,
        'enemies': enemies,
        'special_food': special_food
    }
