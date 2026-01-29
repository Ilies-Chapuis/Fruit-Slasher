import pygame
import os
from button import Button
from settings import Settings
from game import Game
from config import WIDTH, HEIGHT, FPS, get_wallpaper_path


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fruit Ninja Typing")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
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

        # Créer les boutons (sera recréé à chaque changement de langue)
        self.create_buttons()

        # Démarrer la musique si activée
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
            Button(t("difficulty"), 250, 200, 300, 40, self.settings.cycle_difficulty),
            Button(t("language"), 250, 250, 300, 40, self.change_language),
            Button(t("music"), 250, 300, 300, 40, self.settings.toggle_music),
            Button(t("change_music"), 250, 350, 300, 40, self.settings.cycle_music),
            Button(t("back"), 300, 420, 200, 40, self.back)
        ]

    def change_language(self):
        """Change la langue et recrée les boutons"""
        self.settings.cycle_language()
        self.create_buttons()  # Recréer les boutons avec les nouveaux textes

    def start_game(self):
        Game(self.settings).run()
        # Relancer la musique après le jeu si elle était activée
        if self.settings.music:
            self.settings.play_music()

    def open_settings(self):
        self.state = "SETTINGS"

    def back(self):
        self.state = "MAIN"

    def quit(self):
        self.settings.stop_music()
        self.running = False

    def draw_settings_values(self):
        """Affiche les valeurs actuelles des paramètres"""
        t = self.settings.t

        infos = [
            f"{t('difficulty')} : {self.settings.difficulty}",
            f"{t('language')} : {self.settings.language}",
            f"{t('music')} : {'ON' if self.settings.music else 'OFF'}",
            f"Piste : {self.settings.get_current_music_name()}"
        ]

        for i, txt in enumerate(infos):
            rendered = self.font.render(txt, True, (255, 200, 0))
            self.screen.blit(rendered, (260, 160 + i * 50))

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
                self.draw_settings_values()
                for b in self.settings_buttons:
                    b.draw(self.screen, self.font)

            pygame.display.flip()

        pygame.quit()