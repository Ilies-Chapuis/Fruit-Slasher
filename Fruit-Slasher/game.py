import pygame
import random
import os

from fruit import Fruit
from player import Player
from config import *
from settings import Settings


class Game:
    def __init__(self, settings):
        pygame.init()

        self.settings = settings
        self.diff = DIFFICULTY_CONFIG[self.settings.difficulty]

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fruit Ninja Typing")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.title_font = pygame.font.SysFont(None, 64)

        self.player = Player(MAX_LIVES)
        self.fruits = []
        self.current_input = ""
        self.running = True

        # Mode de jeu
        self.game_mode = settings.game_mode

        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, self.diff["spawn_delay"])

        # Charger l'image de fond
        self.background = None
        bg_path = get_wallpaper_path()
        if os.path.exists(bg_path):
            try:
                self.background = pygame.image.load(bg_path)
                self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
                print(f"Wallpaper charge")
            except Exception as e:
                print(f"Erreur wallpaper: {e}")

        # Afficher le mode de jeu
        mode_name = "TYPING" if self.game_mode == "TYPING" else "CLICK"
        print(f"Mode de jeu: {mode_name}")

    def spawn_fruit(self):
        is_bomb = random.random() < self.diff["BOMB_CHANCE"]

        if is_bomb:
            word = BOMB_WORD
            image_path = BOMB_IMAGE
        else:
            word = random.choice(FRUITS)
            image_path = get_fruit_image_path(word)

        x = random.randint(50, WIDTH - 150)
        speed = random.randint(
            self.diff["speed_min"],
            self.diff["speed_max"]
        )

        self.fruits.append(Fruit(word, x, speed, is_bomb, image_path))

    def handle_click(self, pos):
        """Gère les clics sur les fruits (mode CLICK)"""
        for fruit in self.fruits[:]:
            fruit_rect = fruit.get_rect()
            if fruit_rect.collidepoint(pos):
                if fruit.is_bomb:
                    # Pénalité pour cliquer sur une bombe
                    self.player.lose_life()
                    self.player.lose_life()
                else:
                    # Récompense pour cliquer sur un fruit
                    self.player.add_score()
                self.fruits.remove(fruit)
                break

    def handle_input(self, event):
        """Gère la saisie au clavier (mode TYPING)"""
        if event.key == pygame.K_BACKSPACE:
            self.current_input = self.current_input[:-1]
        elif event.key == pygame.K_RETURN:
            self.check_word()
            self.current_input = ""
        else:
            self.current_input += event.unicode

    def check_word(self):
        """Vérifie si le mot tapé correspond à un fruit"""
        for fruit in self.fruits[:]:
            if fruit.word == self.current_input:
                if fruit.is_bomb:
                    self.player.lose_life()
                    self.player.lose_life()
                else:
                    self.player.add_score()
                self.fruits.remove(fruit)
                break

    def update(self):
        for fruit in self.fruits[:]:
            fruit.update()
            if fruit.is_off_screen(HEIGHT):
                if not fruit.is_bomb:
                    self.player.lose_life()
                self.fruits.remove(fruit)

    def draw_ui(self):
        t = self.settings.t

        score = self.font.render(f"{t('score')}: {self.player.score}", True, (255, 255, 255))
        lives = self.font.render(f"{t('lives')}: {self.player.lives}", True, (255, 80, 80))
        combo = self.font.render(f"{t('combo')}: x{self.player.combo}", True, (255, 200, 0))

        self.screen.blit(score, (10, 10))
        self.screen.blit(lives, (10, 40))
        self.screen.blit(combo, (10, 70))

        # Affichage selon le mode
        if self.game_mode == "TYPING":
            # Mode frappe : afficher l'input
            input_surface = pygame.Surface((WIDTH - 20, 50))
            input_surface.set_alpha(200)
            input_surface.fill((30, 30, 30))
            self.screen.blit(input_surface, (10, HEIGHT - 60))

            input_txt = self.font.render(f"> {self.current_input}", True, (0, 255, 0))
            self.screen.blit(input_txt, (20, HEIGHT - 50))
        else:
            # Mode clic : afficher l'instruction
            instruction = self.font.render(t('click_fruits'), True, (255, 255, 0))
            instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 30))
            self.screen.blit(instruction, instruction_rect)

    def draw_game_over(self):
        t = self.settings.t

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        game_over = self.title_font.render(t('game_over'), True, (255, 50, 50))
        final_score = self.font.render(f"{t('score')}: {self.player.score}", True, (255, 255, 255))
        restart_txt = self.font.render("Appuyez sur ESPACE pour continuer", True, (200, 200, 200))

        self.screen.blit(game_over, game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        self.screen.blit(final_score, final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
        self.screen.blit(restart_txt, restart_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80)))

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((20, 20, 20))

        for fruit in self.fruits:
            fruit.draw(self.screen, self.font)

        self.draw_ui()
        pygame.display.flip()

    def run(self):
        self.running = True
        game_over = False

        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == self.SPAWN_EVENT and not game_over:
                    self.spawn_fruit()

                elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    # Mode CLICK : gérer les clics
                    if self.game_mode == "CLICK":
                        self.handle_click(event.pos)

                elif event.type == pygame.KEYDOWN:
                    if game_over:
                        if event.key == pygame.K_SPACE:
                            self.running = False
                    else:
                        # Mode TYPING : gérer la saisie
                        if self.game_mode == "TYPING":
                            self.handle_input(event)

            if not game_over and not self.player.alive():
                game_over = True
                pygame.time.set_timer(self.SPAWN_EVENT, 0)

            if not game_over:
                self.update()
                self.draw()
            else:
                self.draw()
                self.draw_game_over()
                pygame.display.flip()