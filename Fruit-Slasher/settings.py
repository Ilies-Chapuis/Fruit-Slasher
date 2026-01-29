import pygame
import os


class Settings:
    def __init__(self):
        self.difficulty = "NORMAL"
        self.language = "FR"
        self.music = True
        self.music_track = 0  # Index de la piste actuelle

        # Charger les pistes de musique disponibles
        self.music_files = self._load_music_files()

        # Initialiser pygame mixer pour la musique
        try:
            pygame.mixer.init()
            self.music_initialized = True
        except:
            self.music_initialized = False
            print("Erreur: Impossible d'initialiser le systeme audio")

    def _load_music_files(self):
        """Charge la liste des fichiers audio depuis Assets/Music/"""
        music_paths = [
            "./Assets/Music/",
            "Assets/Music/",
            "./Music/",
            "Music/"
        ]

        music_files = []

        for path in music_paths:
            if os.path.exists(path):
                try:
                    files = os.listdir(path)
                    # Chercher les fichiers audio
                    audio_files = [
                        os.path.join(path, f) for f in files
                        if f.endswith(('.mp3', '.wav', '.ogg'))
                    ]
                    if audio_files:
                        music_files = sorted(audio_files)
                        print(f"Musiques trouvees: {len(music_files)} fichiers dans {path}")
                        break
                except:
                    continue

        if not music_files:
            print("Aucune musique trouvee dans Assets/Music/")
            # Fichiers par défaut (au cas où)
            music_files = ["track1.mp3", "track2.mp3", "track3.mp3"]

        return music_files

    def get_current_music_name(self):
        """Retourne le nom de la piste actuelle"""
        if self.music_files and self.music_track < len(self.music_files):
            return os.path.basename(self.music_files[self.music_track])
        return "Aucune"

    def play_music(self):
        """Lance la musique actuelle"""
        if not self.music or not self.music_initialized:
            return

        if self.music_files and self.music_track < len(self.music_files):
            try:
                music_file = self.music_files[self.music_track]
                if os.path.exists(music_file):
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.play(-1)  # -1 = boucle infinie
                    print(f"Lecture: {os.path.basename(music_file)}")
                else:
                    print(f"Fichier introuvable: {music_file}")
            except Exception as e:
                print(f"Erreur lecture musique: {e}")

    def stop_music(self):
        """Arrête la musique"""
        if self.music_initialized:
            try:
                pygame.mixer.music.stop()
            except:
                pass

    # Textes multilingues
    TEXTS = {
        "FR": {
            "play": "Jouer",
            "settings": "Parametres",
            "quit": "Quitter",
            "difficulty": "Difficulte",
            "language": "Langue",
            "music": "Musique",
            "change_music": "Changer musique",
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
            "change_music": "Change music",
            "back": "Back",
            "score": "Score",
            "lives": "Lives",
            "combo": "Combo",
            "game_over": "GAME OVER",
        }
    }

    def t(self, key):
        """Retourne la traduction pour une clé donnée"""
        return self.TEXTS[self.language].get(key, key)

    def cycle_language(self):
        """Change la langue"""
        self.language = "EN" if self.language == "FR" else "FR"

    def cycle_difficulty(self):
        """Change la difficulté"""
        levels = ["FACILE", "NORMAL", "DIFFICILE"]
        self.difficulty = levels[(levels.index(self.difficulty) + 1) % 3]

    def toggle_music(self):
        """Active/désactive la musique"""
        self.music = not self.music
        if self.music:
            self.play_music()
        else:
            self.stop_music()

    def cycle_music(self):
        """Passe à la piste suivante"""
        if self.music_files:
            self.music_track = (self.music_track + 1) % len(self.music_files)
            if self.music:
                self.play_music()