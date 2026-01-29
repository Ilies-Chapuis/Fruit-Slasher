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
    FRUITS_CHANCE = 0.85 #85%
    BOMB_CHANCE = 0.05 #5%
    ICE_CHANCE = 0.10 #10%
    MAX_WINDOW = 7
    MAX_LIVES = 5

elif DIFFICULTY_CONFIG == "Normal":
    FRUITS_CHANCE = 0.65 #65%
    BOMB_CHANCE = 0.15 #15%
    ICE_CHANCE = 0.15 #15%
    GOLDEN_CHANCE = 0.5 #5%
    MAX_WINDOW = 10
    MAX_LIVES = 3

elif DIFFICULTY_CONFIG == "Hard":
    FRUITS_CHANCE = 0.50 #50%
    BOMB_CHANCE = 0.30 #30%
    ICE_CHANCE = 0.5 #5%
    GOLDEN_CHANCE = 0.15 #15%
    MAX_WINDOW = 15
    MAX_LIVES = 3



SPAWN_RATE = 1300
FONT_SIZE = 32