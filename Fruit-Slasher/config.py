import os

WIDTH, HEIGHT = 800, 600
FPS = 60

#  fruits avec leurs images
FRUITS_IMAGES = {
    "apple": "Red_Apple.png",
    "banana": "Banana.png",
    "cherry": "Cherry.png",
    "kiwi": "Kiwi.png",
    "orange": "Orange.png",
    "peach": "Peach.png",
    "pear": "Pear.png",
    "melon": "Melon.png",
    "avocado": "Avocado.png",
    "grapes": "Grapes.png",
    "lemon": "Lemon.png",
    "pineapple": "Pinneaple.png",
    "strawberry": "Strawberry.png",
    "watermelon": "Watermelon.png"
}

FRUITS = list(FRUITS_IMAGES.keys())

# Nom du fichier wallpaper
WALLPAPER_FILENAME = "Fruit Slasher Wallpaper (Bonus).jpg"

BOMB_WORD = "bomb"
BOMB_IMAGE = "Bomb.png"
BOMB_CHANCE = 0.15

FRUIT_SPEED_MIN = 1
FRUIT_SPEED_MAX = 3

SPAWN_DELAY = 1300
MAX_LIVES = 3
FONT_SIZE = 32

FRUIT_IMAGE_SIZE = 80

DIFFICULTY_CONFIG = {
    "FACILE": {
        "speed_min": 1,
        "speed_max": 2,
        "spawn_delay": 1800,
        "FRUITS_CHANCE" : 0.85,  # 85%
        "BOMB_CHANCE" : 0.05 , # 5%
        "ICE_CHANCE" : 0.10,  # 10%
        "MAX_WINDOW" : 7,
        "MAX_LIVES" : 5
    },
    "NORMAL": {
        "speed_min": 2,
        "speed_max": 4,
        "spawn_delay": 1300,
        "FRUITS_CHANCE": 0.65,  # 65%
        "BOMB_CHANCE": 0.15,  # 15%
        "ICE_CHANCE": 0.15,  # 15%
        "GOLDEN_CHANCE": 0.5,  # 5%
        "MAX_WINDOW": 10,
        "MAX_LIVES": 3
    },
    "DIFFICILE": {
        "speed_min": 4,
        "speed_max": 7,
        "spawn_delay": 900,
        "FRUITS_CHANCE": 0.50,  # 50%
        "BOMB_CHANCE": 0.30,  # 30%
        "ICE_CHANCE": 0.5,  # 5%
        "GOLDEN_CHANCE": 0.15,  # 15%
        "MAX_WINDOW": 15,
        "MAX_LIVES": 3
    }
}


def find_assets_path():
    #Trouve automatiquement le chemin vers les images
    possible_paths = [
        "./Assets/Images/",
        "Assets/Images/",
        "./Images/",
        "Images/",
        "./",
        os.path.join(os.path.dirname(__file__), "Fruit-Slasher/Assets/Images"),
        os.path.join(os.path.dirname(__file__), "Assets/Images"),
        os.path.join(os.path.dirname(__file__), "Assets/"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            try:
                files = os.listdir(path)
                test_files = [f for f in files if f.endswith('.png')]
                has_wallpaper = WALLPAPER_FILENAME in files
                print(path)


                if test_files or has_wallpaper:
                    print(f"Images trouvees dans: {path}")
                    if test_files:
                        print(f"  - {len(test_files)} images de fruits")
                    if has_wallpaper:
                        print(f"  - Wallpaper detecte")
                    return path
            except:
                continue

    print("ATTENTION: Aucune image trouvee!")
    return "./"


ASSETS_PATH = find_assets_path()


def get_wallpaper_path():
    #Retourne le chemin complet du wallpaper
    return os.path.join(ASSETS_PATH, WALLPAPER_FILENAME)


def get_fruit_image_path(fruit_name):
    #Retourne le chemin d'une image de fruit
    if fruit_name in FRUITS_IMAGES:
        return os.path.join(ASSETS_PATH, FRUITS_IMAGES[fruit_name])
    return None