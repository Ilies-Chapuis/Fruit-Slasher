WIDTH, HEIGHT = 800, 600
FPS = 60

FRUITS = [
    "apple", "banana", "cherry", "kiwi",
    "orange", "mango", "pear", "melon"
]

BOMB_WORD = "bomb"
BOMB_CHANCE = 0.15  # 15%

FRUIT_SPEED_MIN = 1
FRUIT_SPEED_MAX = 3

SPAWN_DELAY = 1300
MAX_LIVES = 3
FONT_SIZE = 32

DIFFICULTY_CONFIG = {
    "FACILE": {
        "speed_min": 1,
        "speed_max": 2,
        "spawn_delay": 1800,
        "bomb_chance": 0.05
    },
    "NORMAL": {
        "speed_min": 2,
        "speed_max": 4,
        "spawn_delay": 1300,
        "bomb_chance": 0.15
    },
    "DIFFICILE": {
        "speed_min": 4,
        "speed_max": 7,
        "spawn_delay": 900,
        "bomb_chance": 0.30
    }
}
