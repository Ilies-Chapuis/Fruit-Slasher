import pygame
import os
import random


class Fruit:
    def __init__(self, word, x, speed, fruit_type="normal", image_path=None):
        """
        Types de fruits:
        - "normal": fruit standard
        - "bomb": bombe (-2 vies)
        - "golden": fruit bonus (+40 points)
        - "ice": glaçon (gèle l'écran 5 secondes)
        """
        self.word = word
        self.x = x
        self.y = -100
        self.speed = speed
        self.fruit_type = fruit_type
        self.sliced = False

        # Propriétés pour l'animation de découpe
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

        # Particules pour les bombes
        self.particles = []

        # Charger l'image si disponible
        self.image = None
        if image_path:
            if os.path.exists(image_path):
                try:
                    original_image = pygame.image.load(image_path)
                    from config import FRUIT_IMAGE_SIZE
                    self.image = pygame.transform.scale(
                        original_image,
                        (FRUIT_IMAGE_SIZE, FRUIT_IMAGE_SIZE)
                    )
                    print(f"Image chargee: {os.path.basename(image_path)}")
                except Exception as e:
                    print(f"Erreur chargement {image_path}: {e}")
                    self.image = None
            else:
                print(f"Fichier introuvable: {image_path}")

    def cut(self):
        """Coupe le fruit avec animation"""
        if self.sliced:
            return

        self.sliced = True

        if self.fruit_type == "bomb":
            # Créer des particules d'explosion pour la bombe
            for _ in range(25):
                self.particles.append({
                    "pos": [self.x + 40, self.y + 40],
                    "vx": random.randint(-8, 8),
                    "vy": random.randint(-8, -5),
                    "radius": random.randint(5, 10),
                    "color": (255, random.randint(100, 255), 0),
                })
        elif self.image:
            # Créer les deux moitiés du fruit
            from config import FRUIT_IMAGE_SIZE
            self.left_half = pygame.Surface((FRUIT_IMAGE_SIZE // 2, FRUIT_IMAGE_SIZE), pygame.SRCALPHA)
            self.right_half = pygame.Surface((FRUIT_IMAGE_SIZE // 2, FRUIT_IMAGE_SIZE), pygame.SRCALPHA)

            self.left_half.blit(self.image, (0, 0), (0, 0, FRUIT_IMAGE_SIZE // 2, FRUIT_IMAGE_SIZE))
            self.right_half.blit(self.image, (0, 0),
                                 (FRUIT_IMAGE_SIZE // 2, 0, FRUIT_IMAGE_SIZE // 2, FRUIT_IMAGE_SIZE))

            self.left_pos = (self.x + FRUIT_IMAGE_SIZE // 4, self.y + FRUIT_IMAGE_SIZE // 2)
            self.right_pos = (self.x + 3 * FRUIT_IMAGE_SIZE // 4, self.y + FRUIT_IMAGE_SIZE // 2)

            self.left_vx = random.randint(-5, -2)
            self.right_vx = random.randint(2, 5)
            self.left_vy = random.randint(-8, -5)
            self.right_vy = random.randint(-8, -5)

            self.left_rot_speed = random.randint(-5, 5)
            self.right_rot_speed = random.randint(-5, 5)

    def update(self):
        """Met à jour la position du fruit ou ses animations"""
        gravity = 0.4

        if not self.sliced:
            self.y += self.speed
        else:
            if self.fruit_type == "bomb":
                # Mise à jour des particules
                for p in self.particles:
                    p["vy"] += gravity
                    p["pos"][0] += p["vx"]
                    p["pos"][1] += p["vy"]
            elif self.left_half:
                # Mise à jour des moitiés
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

    def draw(self, screen, font):
        """Affiche le fruit ou son animation"""
        if not self.sliced:
            if self.image:
                # Afficher l'image
                screen.blit(self.image, (self.x, self.y))

                # Couleur du texte selon le type
                if self.fruit_type == "bomb":
                    text_color = (255, 50, 50)  # Rouge
                elif self.fruit_type == "golden":
                    text_color = (255, 215, 0)  # Or
                elif self.fruit_type == "ice":
                    text_color = (100, 200, 255)  # Bleu clair
                else:
                    text_color = (255, 255, 255)  # Blanc

                # Afficher le mot en dessous
                text = font.render(self.word, True, text_color)
                text_rect = text.get_rect(center=(self.x + self.image.get_width() // 2,
                                                  self.y + self.image.get_height() + 15))

                # Fond semi-transparent
                text_bg = pygame.Surface((text.get_width() + 10, text.get_height() + 5))
                text_bg.set_alpha(150)
                text_bg.fill((0, 0, 0))
                screen.blit(text_bg, (text_rect.x - 5, text_rect.y - 2))
                screen.blit(text, text_rect)
            else:
                # Fallback: afficher le texte avec symbole
                if self.fruit_type == "bomb":
                    symbol = "X"
                    color = (255, 50, 50)
                elif self.fruit_type == "golden":
                    symbol = "*"
                    color = (255, 215, 0)
                elif self.fruit_type == "ice":
                    symbol = "~"
                    color = (100, 200, 255)
                else:
                    symbol = ""
                    color = (255, 200, 0)

                display_text = f"{symbol}[{self.word}]{symbol}" if symbol else f"[{self.word}]"
                text = font.render(display_text, True, color)
                screen.blit(text, (self.x, self.y))
        else:
            # Afficher l'animation de découpe
            if self.fruit_type == "bomb":
                # Afficher les particules
                for p in self.particles:
                    pygame.draw.circle(screen, p["color"], (int(p["pos"][0]), int(p["pos"][1])), p["radius"])
            elif self.left_half:
                # Afficher les deux moitiés en rotation
                left = pygame.transform.rotate(self.left_half, self.left_rotation)
                right = pygame.transform.rotate(self.right_half, self.right_rotation)
                screen.blit(left, left.get_rect(center=self.left_pos))
                screen.blit(right, right.get_rect(center=self.right_pos))

    def is_off_screen(self, height):
        """Vérifie si le fruit est hors de l'écran"""
        if not self.sliced:
            return self.y > height
        else:
            # Pour les fruits coupés, vérifier si les moitiés sont hors écran
            if self.left_half:
                return self.left_pos[1] > height + 100 and self.right_pos[1] > height + 100
            elif self.particles:
                # Pour les bombes, vérifier si toutes les particules sont hors écran
                return all(p["pos"][1] > height + 50 for p in self.particles)
            return True

    def get_rect(self):
        """Retourne le rectangle de collision"""
        if self.image:
            from config import FRUIT_IMAGE_SIZE
            return pygame.Rect(self.x, self.y, FRUIT_IMAGE_SIZE, FRUIT_IMAGE_SIZE)
        else:
            return pygame.Rect(self.x, self.y, 100, 30)

    # Propriétés pour faciliter les vérifications
    @property
    def is_bomb(self):
        return self.fruit_type == "bomb"

    @property
    def is_golden(self):
        return self.fruit_type == "golden"

    @property
    def is_ice(self):
        return self.fruit_type == "ice"