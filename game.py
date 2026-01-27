import pygame
import random

class Fruit:

    def __init__(self, lettre, x, y):
        self.lettre= lettre
        self.x = x
        self.y = y
        self.vy = random.randint(-8, -5)
        self.vx = random.randint(-3, 3)
        self.est_coupe= False
        self.radius = 30

    def update(self):
        self.vy += 0.5
        self.x += self.vx
        self.y += self.vy

    def draw (self, screen):
        color= (255,0,0) if not self.est_coupe else (128,128,128)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        font = pygame.font.Font(None, 40)
        text= font.render(self.lettre.upper(), True, (255,255,255))
        screen.blit(text, (self.x -10, self.y -15))

    def spawn_fruit(fruits):
        lettre = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        x = random.randint(50, 750)
        y= 600
        fruits.append(Fruit(lettre, x, y))

    def handle_input(fruits, event):
        if event.type == pygame.KEYDOWN:
            for fruit in fruits:
                if not fruit.est_coupe and event.unicode.upper() == fruits.lettre:
                    fruit.est_coupe = True