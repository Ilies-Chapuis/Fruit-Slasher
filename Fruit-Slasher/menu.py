import pygame
import os
from button import Button
from settings import Settings
from config import WIDTH, HEIGHT, FPS, get_wallpaper_path


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fruit Ninja Typing")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 72)

        self.settings = Settings()
        self.state = "MAIN"
        self.running = True

        # Charger le wallpaper
        self.background = None
        bg_path = get_wallpaper_path()
        if os.path.exists(bg_path):
            try:
                self.background = pygame.image.load(bg_path)
                self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
                print(f"Wallpaper menu charge")
            except Exception as e:
                print(f"Erreur wallpaper menu: {e}")

        self.create_buttons()

        # Démarrer la musique
        if self.settings.music:
            self.settings.play_music()

    def create_buttons(self):
        """Crée les boutons avec les textes dans la langue actuelle"""
        t = self.settings.t

        self.main_buttons = [
            Button(t("play"), 300, 200, 200, 50, self.start_game),
            Button(t("settings"), 300, 270, 200, 50, self.open_settings),
            Button(t("quit"), 300, 340, 200, 50, self.quit)
        ]

        self.settings_buttons = [
            Button(t("difficulty"), 220, 160, 360, 35, self.change_difficulty),
            Button(t("game_mode"), 220, 205, 360, 35, self.change_game_mode),
            Button(t("keyboard"), 220, 250, 360, 35, self.change_keyboard),
            Button(t("language"), 220, 295, 360, 35, self.change_language),
            Button(t("music"), 220, 340, 360, 35, self.toggle_music),
            Button(t("change_music"), 220, 385, 360, 35, self.change_music_track),
            Button(t("back"), 300, 450, 200, 40, self.back)
        ]

    def change_difficulty(self):
        """Change la difficulté"""
        self.settings.cycle_difficulty()
        print(f"Difficulte changee: {self.settings.difficulty}")

    def change_game_mode(self):
        """Change le mode de jeu"""
        self.settings.cycle_game_mode()
        print(f"Mode de jeu change: {self.settings.game_mode}")

    def change_keyboard(self):
        """Change le clavier"""
        self.settings.cycle_keyboard()
        print(f"Clavier change: {self.settings.keyboard_layout}")

    def change_language(self):
        """Change la langue et recrée les boutons"""
        self.settings.cycle_language()
        print(f"Langue changee: {self.settings.language}")
        self.create_buttons()

    def toggle_music(self):
        """Active/désactive la musique"""
        self.settings.toggle_music()
        print(f"Musique: {'ON' if self.settings.music else 'OFF'}")

    def change_music_track(self):
        """Change la piste de musique"""
        self.settings.cycle_music()
        print(f"Piste changee: {self.settings.get_current_music_name()}")

    def start_game(self):
        """Lance le jeu - import ici pour éviter l'import circulaire"""
        from game import Game
        Game(self.settings).run()
        # Relancer la musique après le jeu
        if self.settings.music:
            self.settings.play_music()

    def open_settings(self):
        self.state = "SETTINGS"
        print("Ouverture des parametres")

    def back(self):
        self.state = "MAIN"
        print("Retour au menu principal")

    def quit(self):
        self.settings.stop_music()
        self.running = False

    def draw_settings_values(self):
        """Affiche les valeurs actuelles des paramètres"""
        t = self.settings.t

        # Mode de jeu avec description
        mode_display = t("typing_mode") if self.settings.game_mode == "TYPING" else t("click_mode")

        infos = [
            f"{t('difficulty')} : {self.settings.difficulty}",
            f"{t('game_mode')} : {mode_display}",
            f"{t('keyboard')} : {self.settings.keyboard_layout}",
            f"{t('language')} : {self.settings.language}",
            f"{t('music')} : {'ON' if self.settings.music else 'OFF'}",
            f"Piste : {self.settings.get_current_music_name()}"
        ]

        for i, txt in enumerate(infos):
            rendered = self.small_font.render(txt, True, (255, 200, 0))
            self.screen.blit(rendered, (230, 125 + i * 45))

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            # Afficher le fond
            if self.background:
                self.screen.blit(self.background, (0, 0))
                # Overlay pour lisibilite
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(100)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))
            else:
                self.screen.fill((15, 15, 15))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                buttons = self.main_buttons if self.state == "MAIN" else self.settings_buttons
                for b in buttons:
                    b.handle_event(event)

            if self.state == "MAIN":
                # Titre
                title = self.title_font.render("FRUIT NINJA", True, (255, 100, 50))
                title_rect = title.get_rect(center=(WIDTH // 2, 100))

                # Ombre
                title_shadow = self.title_font.render("FRUIT NINJA", True, (0, 0, 0))
                self.screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
                self.screen.blit(title, title_rect)

                for b in self.main_buttons:
                    b.draw(self.screen, self.font)

            else:
                # Titre des paramètres
                settings_title = self.font.render(self.settings.t("settings"), True, (255, 150, 50))
                self.screen.blit(settings_title, settings_title.get_rect(center=(WIDTH // 2, 60)))

                self.draw_settings_values()
                for b in self.settings_buttons:
                    b.draw(self.screen, self.small_font)

            pygame.display.flip()

        pygame.quit()