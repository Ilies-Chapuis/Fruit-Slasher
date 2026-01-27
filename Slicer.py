import pygame
import random

# ======================
# CLASSE FRUIT
# ======================
class Fruit:

    # Permet de créer un fruit
    def __init__(self, lettre, x, y):
        self.lettre = lettre
        self.x = x
        self.y = y
        self.vy = random.randint(-16, -16)   # vitesse verticale (lancé vers le haut)
        self.vx = random.randint(-3, 3)    # vitesse horizontale
        self.est_coupe = False
        self.radius = 30                   # taille du fruit

    # Permet de gérer le mouvement du fruit
    def update(self):
        self.vy += 0.4     # gravité
        self.x += self.vx
        self.y += self.vy

    # Permet d'afficher le fruit
    def draw(self, screen):
        color = (255, 0, 0) if not self.est_coupe else (128, 128, 128)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

        font = pygame.font.Font(None, 40)
        text = font.render(self.lettre.upper(), True, (255, 255, 255))
        screen.blit(text, (self.x - 10, self.y - 15))


# ======================
# FONCTIONS DU JEU
# ======================

# Permet de générer un fruit
def spawn_fruit(fruits):
    lettre = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    x = random.randint(50, 750)
    y = 600  # fait apparaître le fruit en bas de l'écran
    fruits.append(Fruit(lettre, x, y))


# Permet de détecter les touches du clavier pour couper les fruits
def handle_input(fruits, event):
    if event.type == pygame.KEYDOWN:
        for fruit in fruits:
            if not fruit.est_coupe and event.unicode.upper() == fruit.lettre:
                fruit.est_coupe = True
                # ici tu peux ajouter un son, des points, etc.


# ======================
# INITIALISATION PYGAME
# ======================
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fruit Ninja Clavier")
clock = pygame.time.Clock()

fruits = []
running = True
spawn_timer = 0


# ======================
# BOUCLE PRINCIPALE
# ======================
while running:
    screen.fill((0, 0, 0))

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handle_input(fruits, event)

    # Génération automatique des fruits
    spawn_timer += 1
    if spawn_timer > 60:  # environ 1 fruit par seconde
        spawn_fruit(fruits)
        spawn_timer = 0

    # Mise à jour et affichage des fruits
    for fruit in fruits:
        fruit.update()
        fruit.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
