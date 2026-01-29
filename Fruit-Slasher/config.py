import os

WIDTH, HEIGHT = 800, 600
FPS = 60

#  fruits avec leurs images
FRUITS_IMAGES = {
    "apple": "Images_Red_Apple.png",
    "banana": "Images_Banana.png",
    "cherry": "Images_Cherry.png",
    "kiwi": "Images_Kiwi.png",
    "orange": "Images_Orange.png",
    "peach": "Images_Peach.png",
    "pear": "Images_Pear.png",
    "melon": "Images_Melon.png",
    "avocado": "Images_Avocado.png",
    "grapes": "Images_Grapes.png",
    "lemon": "Images_Lemon.png",
    "pineapple": "Images_Pinneaple.png",
    "strawberry": "Images_Strawberry.png",
    "watermelon": "Images_Watermelon.png"
}

FRUITS = list(FRUITS_IMAGES.keys())

# Nom du fichier wallpaper
WALLPAPER_FILENAME = "Fruit_Slasher_Wallpaper__Base_.png"

BOMB_WORD = "bomb"
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


def find_assets_path():
    #Trouve automatiquement le chemin vers les images
    possible_paths = [
        "./Fruit-Slasher/Assets/Images",
        "./Assets/Images/",
        "Assets/Images/",
        "./Assets/",
        "Assets/",
        "./Images/",
        "Images/",
        "./",
        os.path.join(os.path.dirname(__file__), "Fruit-Slasher/Assets/Images"),
        os.path.join(os.path.dirname(__file__), "Assets/Images/"),
        os.path.join(os.path.dirname(__file__), "Assets/"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            try:
                files = os.listdir(path)
                test_files = [f for f in files if f.startswith('Images_') and f.endswith('.png')]
                has_wallpaper = WALLPAPER_FILENAME in files

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