import pygame
from button import Button
from settings import Settings
from game import Game
from config import WIDTH, HEIGHT, FPS

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fruit Ninja Typing")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.settings = Settings()
        self.state = "MAIN"
        self.running = True

        self.create_buttons()

    def create_buttons(self):
        self.main_buttons = [
            Button("Jouer", 300, 200, 200, 50, self.start_game),
            Button("Paramètres", 300, 270, 200, 50, self.open_settings),
            Button("Quitter", 300, 340, 200, 50, self.quit)
        ]

        self.settings_buttons = [
            Button("Difficulté", 250, 200, 300, 40, self.settings.cycle_difficulty),
            Button("Langue", 250, 250, 300, 40, self.settings.cycle_language),
            Button("Musique", 250, 300, 300, 40, self.settings.toggle_music),
            Button("Changer musique", 250, 350, 300, 40, self.settings.cycle_music),
            Button("Retour", 300, 420, 200, 40, self.back)
        ]

    def start_game(self):
        Game(self.settings).run()

    def open_settings(self):
        self.state = "SETTINGS"

    def back(self):
        self.state = "MAIN"

    def quit(self):
        self.running = False

    def draw_settings_values(self):
        infos = [
            f"Difficulté : {self.settings.difficulty}",
            f"Langue : {self.settings.language}",
            f"Musique : {'ON' if self.settings.music else 'OFF'}",
            f"Piste : {self.settings.music_track}"
        ]

        for i, txt in enumerate(infos):
            t = self.font.render(txt, True, (255, 200, 0))
            self.screen.blit(t, (260, 160 + i * 50))

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.screen.fill((15, 15, 15))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                buttons = self.main_buttons if self.state == "MAIN" else self.settings_buttons
                for b in buttons:
                    b.handle_event(event)

            if self.state == "MAIN":
                for b in self.main_buttons:
                    b.draw(self.screen, self.font)

            else:
                self.draw_settings_values()
                for b in self.settings_buttons:
                    b.draw(self.screen, self.font)

            pygame.display.flip()

        pygame.quit()
