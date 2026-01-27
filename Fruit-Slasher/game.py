import pygame
import random

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
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)

        self.player = Player(MAX_LIVES)
        self.fruits = []
        self.current_input = ""
        self.running = True

        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, self.diff["spawn_delay"])

    def spawn_fruit(self):
        is_bomb = random.random() < self.diff["bomb_chance"]

        word = "bomb" if is_bomb else random.choice(FRUITS)
        x = random.randint(50, WIDTH - 150)
        speed = random.randint(
            self.diff["speed_min"],
            self.diff["speed_max"]
        )

        self.fruits.append(Fruit(word, x, speed, is_bomb))

    def handle_input(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.current_input = self.current_input[:-1]
        elif event.key == pygame.K_RETURN:
            self.check_word()
            self.current_input = ""
        else:
            self.current_input += event.unicode

    def check_word(self):
        for fruit in self.fruits:
            if fruit.word == self.current_input:
                self.player.add_score()
                self.fruits.remove(fruit)
                break

    def update(self):
        for fruit in self.fruits[:]:
            fruit.update()
            if fruit.is_off_screen(HEIGHT):
                self.player.lose_life()
                self.fruits.remove(fruit)

    def draw_ui(self):
        t = self.settings.t

        score = self.font.render(f"{t('score')}: {self.player.score}", True, (255, 255, 255))
        lives = self.font.render(f"{t('lives')}: {self.player.lives}", True, (255, 80, 80))
        combo = self.font.render(f"{t('combo')}: x{self.player.combo}", True, (255, 200, 0))
        input_txt = self.font.render(self.current_input, True, (0, 255, 0))

        self.screen.blit(score, (10, 10))
        self.screen.blit(lives, (10, 40))
        self.screen.blit(combo, (10, 70))
        self.screen.blit(input_txt, (10, HEIGHT - 40))

    def draw(self):
        self.screen.fill((20, 20, 20))

        for fruit in self.fruits:
            fruit.draw(self.screen, self.font)

        self.draw_ui()
        pygame.display.flip()

    def run(self):
        self.running = True

        while self.running and self.player.alive():
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == self.SPAWN_EVENT:
                    self.spawn_fruit()

                elif event.type == pygame.KEYDOWN:
                    self.handle_input(event)

            self.update()
            self.draw()




