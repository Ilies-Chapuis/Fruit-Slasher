class Settings:
    def __init__(self):
        self.difficulty = "NORMAL"
        self.language = "FR"
        self.music = True
        self.music_track = "track1"

    def toggle_music(self):
        self.music = not self.music

    def cycle_difficulty(self):
        levels = ["FACILE", "NORMAL", "DIFFICILE"]
        self.difficulty = levels[(levels.index(self.difficulty) + 1) % 3]

    def cycle_language(self):
        self.language = "EN" if self.language == "FR" else "FR"

    def cycle_music(self):
        tracks = ["track1", "track2", "track3"]
        self.music_track = tracks[(tracks.index(self.music_track) + 1) % 3]