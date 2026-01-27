class Settings:
    def __init__(self):
        self.difficulty = "NORMAL"
        self.language = "FR"
        self.music = True
        self.music_track = "track1"

    # --------- Language ---------
    TEXTS = {
        "FR": {
            "play": "Jouer",
            "settings": "Paramètres",
            "quit": "Quitter",
            "difficulty": "Difficulté",
            "language": "Langue",
            "music": "Musique",
            "back": "Retour",
            "score": "Score",
            "lives": "Vies",
            "combo": "Combo",
            "game_over": "GAME OVER",
        },
        "EN": {
            "play": "Play",
            "settings": "Settings",
            "quit": "Quit",
            "difficulty": "Difficulty",
            "language": "Language",
            "music": "Music",
            "back": "Back",
            "score": "Score",
            "lives": "Lives",
            "combo": "Combo",
            "game_over": "GAME OVER",
        }
    }

    def t(self, key):
        return self.TEXTS[self.language][key]

    def cycle_language(self):
        self.language = "EN" if self.language == "FR" else "FR"

    # --------- Difficulty ---------
    def cycle_difficulty(self):
        levels = ["FACILE", "NORMAL", "DIFFICILE"]
        self.difficulty = levels[(levels.index(self.difficulty) + 1) % 3]

    def toggle_music(self):
        self.music = not self.music


    def cycle_music(self):
        tracks = ["track1", "track2", "track3"]
        self.music_track = tracks[(tracks.index(self.music_track) + 1) % 3]
