import pygame
import random

# ======================
# LISTE DES IMAGES DE FRUITS
# ======================
FRUIT_IMAGES = [
    "assets_fruits/apple.png",
    "assets_fruits/banana.png",
    "assets_fruits/cherry.png",
    "assets_fruits/grape.png",
    "assets_fruits/kiwi.png",
    "assets_fruits/lemon.png",
    "assets_fruits/orange.png",
    "assets_fruits/peach.png",
    "assets_fruits/pear.png",
    "assets_fruits/pineapple.png",
    "assets_fruits/strawberry.png",
    "assets_fruits/watermelon.png",
]

# ======================
# DIFFICULTÉ
# ======================
difficulty = "normal"  # "facile", "normal", "difficile"

# ======================
# INIT PYGAME
# ======================
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fruit Slasher")
clock = pygame.time.Clock()

# ======================
# BACKGROUND 
# ======================
background = pygame.image.load(
    "Fond_Gameplay/Fruit_Slasher_Wallpaper_Bonus.jpg"
).convert()
background = pygame.transform.scale(background, (800, 600))

# ======================
# CLASSES
# ======================
class Fruit:
    def __init__(self, lettre, x, y, image_path):
        self.type = "fruit"
        self.image = pygame.transform.scale(
            pygame.image.load(image_path).convert_alpha(), (70, 70)
        )
        self.lettre = lettre
        self.x = x
        self.y = y
        self.vy = random.randint(-18, -14)
        self.vx = random.randint(-3, 3)
        self.est_coupe = False

        self.left_half = None
        self.right_half = None
        self.left_pos = (0, 0)
        self.right_pos = (0, 0)
        self.left_vx = 0
        self.right_vx = 0
        self.left_vy = 0
        self.right_vy = 0
        self.left_rotation = 0
        self.right_rotation = 0
        self.left_rot_speed = 0
        self.right_rot_speed = 0

    def update(self):
        gravity = 0.4
        if difficulty == "facile":
            gravity = 0.3
        elif difficulty == "difficile":
            gravity = 0.5

        if not self.est_coupe:
            self.vy += gravity
            self.x += self.vx
            self.y += self.vy
        else:
            self.left_vy += gravity
            self.right_vy += gravity
            self.left_pos = (
                self.left_pos[0] + self.left_vx,
                self.left_pos[1] + self.left_vy,
            )
            self.right_pos = (
                self.right_pos[0] + self.right_vx,
                self.right_pos[1] + self.right_vy,
            )
            self.left_rotation += self.left_rot_speed
            self.right_rotation += self.right_rot_speed

    def draw(self, screen):
        if not self.est_coupe:
            screen.blit(self.image, (self.x - 35, self.y - 35))
            font = pygame.font.Font(None, 40)

            if self.type in ["fruit", "ice"]:
                for dx in [-2, -1, 0, 1, 2]:
                    for dy in [-2, -1, 0, 1, 2]:
                        if dx != 0 or dy != 0:
                            outline = font.render(self.lettre.upper(), True, (255, 0, 0))
                            screen.blit(outline, (self.x - 10 + dx, self.y - 15 + dy))

                text = font.render(self.lettre.upper(), True, (255, 255, 255))
                screen.blit(text, (self.x - 10, self.y - 15))
            else:
                text = font.render(self.lettre.upper(), True, (255, 255, 255))
                screen.blit(text, (self.x - 10, self.y - 15))
        else:
            if self.left_half:
                left = pygame.transform.rotate(self.left_half, self.left_rotation)
                right = pygame.transform.rotate(self.right_half, self.right_rotation)
                screen.blit(left, left.get_rect(center=self.left_pos))
                screen.blit(right, right.get_rect(center=self.right_pos))

    def cut(self):
        if self.est_coupe:
            return
        self.est_coupe = True

        self.left_half = pygame.Surface((35, 70), pygame.SRCALPHA)
        self.right_half = pygame.Surface((35, 70), pygame.SRCALPHA)

        self.left_half.blit(self.image, (0, 0), (0, 0, 35, 70))
        self.right_half.blit(self.image, (0, 0), (35, 0, 35, 70))

        self.left_pos = (self.x - 17, self.y)
        self.right_pos = (self.x + 17, self.y)

        self.left_vx = random.randint(-5, -2)
        self.right_vx = random.randint(2, 5)
        self.left_vy = random.randint(-8, -5)
        self.right_vy = random.randint(-8, -5)

        self.left_rot_speed = random.randint(-5, 5)
        self.right_rot_speed = random.randint(-5, 5)

class Bomb(Fruit):
    def __init__(self, lettre, x, y, image_path):
        super().__init__(lettre, x, y, image_path)
        self.type = "bomb"

    def cut(self):
        if self.est_coupe:
            return
        self.est_coupe = True
        self.particles = []

        for _ in range(25):
            self.particles.append({
                "pos": [self.x, self.y],
                "vx": random.randint(-8, 8),
                "vy": random.randint(-8, -5),
                "radius": random.randint(5, 10),
                "color": (255, random.randint(100, 255), 0),
            })

    def update(self):
        if not self.est_coupe:
            self.vy += 0.4
            self.x += self.vx
            self.y += self.vy
        else:
            for p in self.particles:
                p["vy"] += 0.4
                p["pos"][0] += p["vx"]
                p["pos"][1] += p["vy"]

    def draw(self, screen):
        if self.est_coupe:
            for p in self.particles:
                pygame.draw.circle(screen, p["color"], p["pos"], p["radius"])
        else:
            super().draw(screen)

class CubeDeGlace(Fruit):
    def __init__(self, lettre, x, y, image_path):
        super().__init__(lettre, x, y, image_path)
        self.type = "ice"

    def cut(self):
        if self.est_coupe:
            return
        self.est_coupe = True
        return "freeze"

# ======================
# LETTRE UNIQUE
# ======================
def get_unique_letter(fruits):
    used = [f.lettre for f in fruits if not f.est_coupe]
    available = [l for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if l not in used]
    return random.choice(available if available else "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# ======================
# SPAWN
# ======================
def spawn_fruit(fruits):
    lettre = get_unique_letter(fruits)
    x = random.randint(100, 700)
    y = 600
    choice = random.choice(["fruit", "fruit", "bomb", "ice"])

    if choice == "bomb":
        fruits.append(Bomb(lettre, x, y, "assets_fruits/Bomb.PNG"))
    elif choice == "ice":
        fruits.append(CubeDeGlace(lettre, x, y, "assets_fruits/ice.png"))
    else:
        fruits.append(Fruit(lettre, x, y, random.choice(FRUIT_IMAGES)))

# ======================
# VARIABLES
# ======================
fruits = []
spawn_timer = 0
running = True

game_over = False
freeze = False
freeze_time = 0
FREEZE_DURATION = 3000

lives = 3
score = 0

combo_count = 0
combo_timer = 0
COMBO_DURATION = 3000

replay_button = pygame.Rect(300, 350, 200, 60)
bomb_explosion_time = 0
BOMB_DELAY = 800

# ======================
# BOUCLE PRINCIPALE
# ======================
while running:
    screen.blit(background, (0, 0))
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif not game_over and event.type == pygame.KEYDOWN:
            for fruit in fruits:
                if not fruit.est_coupe and event.unicode.upper() == fruit.lettre:
                    effect = fruit.cut()
                    combo_count += 1
                    combo_timer = current_time

                    if fruit.type == "bomb":
                        bomb_explosion_time = current_time + BOMB_DELAY
                    if effect == "freeze":
                        freeze = True
                        freeze_time = current_time
                    if fruit.type == "fruit":
                        score += 1

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if replay_button.collidepoint(event.pos):
                fruits.clear()
                score = 0
                lives = 3
                freeze = False
                spawn_timer = 0
                combo_count = 0
                game_over = False

    if freeze and current_time - freeze_time > FREEZE_DURATION:
        freeze = False

    if bomb_explosion_time and current_time >= bomb_explosion_time:
        game_over = True
        bomb_explosion_time = 0

    if combo_count and current_time - combo_timer > COMBO_DURATION:
        if combo_count > 1:
            score += combo_count
        combo_count = 0

    spawn_speed = 90 if difficulty == "facile" else 60 if difficulty == "normal" else 40

    if not game_over:
        spawn_timer += 1
        if spawn_timer > spawn_speed:
            spawn_fruit(fruits)
            spawn_timer = 0

    for fruit in fruits[:]:
        if not game_over and not freeze:
            fruit.update()
        fruit.draw(screen)

        if not fruit.est_coupe and fruit.y > 600:
            if fruit.type == "fruit":
                lives -= 1
            fruits.remove(fruit)

    if lives <= 0:
        game_over = True

    font = pygame.font.Font(None, 40)
    screen.blit(font.render(f"Vies : {lives}", True, (255, 255, 255)), (10, 10))
    screen.blit(font.render(f"Score : {score}", True, (255, 255, 255)), (650, 10))

    if combo_count > 1:
        combo_font = pygame.font.Font(None, 50)
        screen.blit(combo_font.render(f"COMBO x{combo_count}", True, (255, 255, 0)), (300, 50))

    if game_over:
        font_go = pygame.font.Font(None, 100)
        screen.blit(font_go.render("GAME OVER", True, (255, 0, 0)), (200, 250))
        pygame.draw.rect(screen, (200, 200, 200), replay_button)
        btn_font = pygame.font.Font(None, 40)
        screen.blit(btn_font.render("REJOUER", True, (0, 0, 0)),
                    (replay_button.x + 40, replay_button.y + 15))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
