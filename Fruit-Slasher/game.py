import pygame
import random
import os

from fruit import Fruit
from player import Player
from config import *
from settings import Settings
from scores import ScoreManager


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

        self.player = Player(self.diff.get("MAX_LIVES", MAX_LIVES))
        self.fruits = []
        self.current_input = ""
        self.running = True

        # Mode de jeu
        self.game_mode = settings.game_mode

        # Système de gel
        self.frozen = False
        self.freeze_start_time = 0
        self.freeze_duration = 5000  # 5 secondes en millisecondes

        # Gestionnaire de scores
        self.score_manager = ScoreManager()

        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, self.diff["spawn_delay"])

        # Charger le fond
        self.background = None
        bg_path = get_wallpaper_path()
        if os.path.exists(bg_path):
            try:
                self.background = pygame.image.load(bg_path)
                self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
                print(f"Wallpaper charge")
            except Exception as e:
                print(f"Erreur wallpaper: {e}")

        mode_name = "TYPING" if self.game_mode == "TYPING" else "CLICK"
        print(f"Mode de jeu: {mode_name}")

    def spawn_fruit(self):
        """Génère un fruit selon les probabilités de la difficulté"""
        rand = random.random()

        # Récupérer les probabilités
        bomb_chance = self.diff.get("BOMB_CHANCE", 0.15)
        ice_chance = self.diff.get("ICE_CHANCE", 0.10)
        golden_chance = self.diff.get("GOLDEN_CHANCE", 0.05)

        # Déterminer le type
        if rand < bomb_chance:
            # Bombe
            fruit_type = "bomb"
            word = BOMB_WORD
            image_path = BOMB_IMAGE
        elif rand < bomb_chance + ice_chance:
            # Glaçon
            fruit_type = "ice"
            word = "ice"
            image_path = ICE_IMAGE
        elif rand < bomb_chance + ice_chance + golden_chance:
            # Fruit bonus (golden)
            fruit_type = "golden"
            word = "bonus"  # Mot spécial pour le bonus
            image_path = GOLDEN_IMAGE
        else:
            # Fruit normal
            fruit_type = "normal"
            word = random.choice(FRUITS)
            image_path = get_fruit_image_path(word)

        x = random.randint(50, WIDTH - 150)
        speed = random.randint(
            self.diff["speed_min"],
            self.diff["speed_max"]
        )

        self.fruits.append(Fruit(word, x, speed, fruit_type, image_path))

    def handle_click(self, pos):
        """Gère les clics (mode CLICK)"""
        for fruit in self.fruits[:]:
            fruit_rect = fruit.get_rect()
            if fruit_rect.collidepoint(pos):
                self.handle_fruit_action(fruit)
                break

    def handle_input(self, event):
        """Gère le clavier (mode TYPING)"""
        if event.key == pygame.K_BACKSPACE:
            self.current_input = self.current_input[:-1]
        elif event.key == pygame.K_RETURN:
            self.check_word()
            self.current_input = ""
        else:
            self.current_input += event.unicode

    def check_word(self):
        """Vérifie le mot tapé"""
        for fruit in self.fruits[:]:
            if fruit.word == self.current_input:
                self.handle_fruit_action(fruit)
                break

    def handle_fruit_action(self, fruit):
        """Gère l'action selon le type de fruit coupé"""
        if fruit.is_bomb:
            # Bombe: -2 vies
            self.player.lose_life()
            self.player.lose_life()
            print("BOOM! -2 vies")
        elif fruit.is_golden:
            # Fruit bonus: +40 points (sans combo)
            self.player.score += 40
            print(f"BONUS! +40 points! Total: {self.player.score}")
        elif fruit.is_ice:
            # Glaçon: active le gel
            self.activate_freeze()
            print("ICE! Ecran gele pendant 5 secondes!")
        else:
            # Fruit normal: score avec combo
            self.player.add_score()

        self.fruits.remove(fruit)

    def activate_freeze(self):
        """Active le gel de l'écran"""
        self.frozen = True
        self.freeze_start_time = pygame.time.get_ticks()

    def update(self):
        # Vérifier si le gel est terminé
        if self.frozen:
            elapsed = pygame.time.get_ticks() - self.freeze_start_time
            if elapsed >= self.freeze_duration:
                self.frozen = False
                print("Fin du gel!")

        # Si gelé, ne pas mettre à jour les fruits
        if not self.frozen:
            for fruit in self.fruits[:]:
                fruit.update()
                if fruit.is_off_screen(HEIGHT):
                    # Perdre une vie sauf pour les bombes et glaçons
                    if not fruit.is_bomb and not fruit.is_ice:
                        self.player.lose_life()
                    self.fruits.remove(fruit)

    def draw_ui(self):
        t = self.settings.t

        score_text = self.font.render(f"{t('score')}: {self.player.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"{t('lives')}: {self.player.lives}", True, (255, 80, 80))
        combo_text = self.font.render(f"{t('combo')}: x{self.player.combo}", True, (255, 200, 0))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        self.screen.blit(combo_text, (10, 70))

        # Indicateur de gel
        if self.frozen:
            remaining = (self.freeze_duration - (pygame.time.get_ticks() - self.freeze_start_time)) / 1000
            freeze_text = self.font.render(f"GEL: {remaining:.1f}s", True, (100, 200, 255))
            freeze_rect = freeze_text.get_rect(topright=(WIDTH - 10, 10))
            self.screen.blit(freeze_text, freeze_rect)

        # Affichage selon le mode
        if self.game_mode == "TYPING":
            # Zone de saisie
            input_surface = pygame.Surface((WIDTH - 20, 50))
            input_surface.set_alpha(200)
            input_surface.fill((30, 30, 30))
            self.screen.blit(input_surface, (10, HEIGHT - 60))

            input_text = self.font.render(f"> {self.current_input}", True, (0, 255, 0))
            self.screen.blit(input_text, (20, HEIGHT - 50))
        else:
            # Instruction clic
            instruction = self.font.render(t('click_fruits'), True, (255, 255, 0))
            instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 30))
            self.screen.blit(instruction, instruction_rect)

    def draw_game_over(self):
        t = self.settings.t

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.title_font.render(t('game_over'), True, (255, 50, 50))
        final_score_text = self.font.render(f"{t('score')}: {self.player.score}", True, (255, 255, 255))

        # Vérifier si c'est un high score
        if self.score_manager.is_high_score(self.player.score):
            highscore_text = self.font.render("NOUVEAU HIGH SCORE!", True, (255, 215, 0))
            self.screen.blit(highscore_text, highscore_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))

        restart_text = self.font.render("Appuyez sur ESPACE pour continuer", True, (200, 200, 200))

        self.screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        self.screen.blit(final_score_text, final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80)))

    def draw(self):
        # Fond
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((20, 20, 20))

        # Effet visuel de gel
        if self.frozen:
            ice_overlay = pygame.Surface((WIDTH, HEIGHT))
            ice_overlay.set_alpha(30)
            ice_overlay.fill((100, 200, 255))
            self.screen.blit(ice_overlay, (0, 0))

        # Dessiner les fruits
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
                    if self.game_mode == "CLICK":
                        self.handle_click(event.pos)

                elif event.type == pygame.KEYDOWN:
                    if game_over:
                        if event.key == pygame.K_SPACE:
                            # Sauvegarder le score
                            self.score_manager.save_score(
                                "Joueur",
                                self.player.score,
                                self.settings.difficulty,
                                self.settings.game_mode
                            )
                            self.running = False
                    else:
                        if self.game_mode == "TYPING":
                            self.handle_input(event)

            if not game_over and not self.player.alive():
                game_over = True
                pygame.time.set_timer(self.SPAWN_EVENT, 0)
                print(f"Game Over! Score final: {self.player.score}")

            if not game_over:
                self.update()
                self.draw()
            else:
                self.draw()
                self.draw_game_over()
                pygame.display.flip()