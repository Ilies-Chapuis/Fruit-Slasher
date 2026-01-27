WIDTH, HEIGHT = 800, 600
FPS = 60

FRUITS = [
    "Avocado", "Banana", "Cherry", "Grapes", "Green Apple", "Kiwi", "Lemon", "Melon", "Orange", "Peach", "Pear", "Pinneaple", "Red Apple", "Strawberry", "Watermelon"
]
BOMB = ["Bomb"]
ICE_CUBE = ["Ice Cube"]
GOLDEN = ["Golden Fruit"]

DIFFICULTY_CONFIG =  "Easy", "Normal", "Hard"

if DIFFICULTY_CONFIG == "Easy":
    FRUITS_CHANCE = 0.85
    FRUITS_SPEED_MIN =
    FRUITS_SPEED_MAX =
    BOMB_CHANCE = 0.05
    BOMB_SPEED_MIN =
    BOMB_SPEED_MAX =
    ICE_CHANCE = 0.10
    ICE_SPEED_MIN =
    ICE_SPEED_MAX =
    GENERAL_SPAWN_RATE =
    MAX_WINDOW = 7
    MAX_LIVES = 5

elif DIFFICULTY_CONFIG == "Normal":
    FRUITS_CHANCE = 0.65
    FRUITS_SPEED_MIN =
    FRUITS_SPEED_MAX =
    BOMB_CHANCE = 0.15
    BOMB_SPEED_MIN =
    BOMB_SPEED_MAX =
    ICE_CHANCE = 0.15
    ICE_SPEED_MIN =
    ICE_SPEED_MAX =
    GOLDEN_CHANCE = 0.5
    GOLDEN_SPEED_MIN =
    GOLDEN_SPEED_MAX =
    GENERAL_SPAWN_RATE =
    MAX_WINDOW = 10
    MAX_LIVES = 3

elif DIFFICULTY_CONFIG == "Hard":
    FRUITS_CHANCE = 0.50
    FRUITS_SPEED_MIN =
    FRUITS_SPEED_MAX =
    BOMB_CHANCE = 0.30
    BOMB_SPEED_MIN =
    BOMB_SPEED_MAX =
    ICE_CHANCE = 0.5
    ICE_SPEED_MIN =
    ICE_SPEED_MAX =
    GOLDEN_CHANCE = 0.15
    GOLDEN_SPEED_MIN =
    GOLDEN_SPEED_MAX =
    GENERAL_SPAWN_RATE =
    MAX_WINDOW = 15
    MAX_LIVES = 3



SPAWN_RATE = 1300
FONT_SIZE = 32