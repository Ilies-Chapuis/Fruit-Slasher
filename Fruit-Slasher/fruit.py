import pygame
import os


class Fruit:
    def __init__(self, word, x, speed, is_bomb=False, image_path=None):
        self.word = word
        self.x = x
        self.y = -100
        self.speed = speed
        self.is_bomb = is_bomb
        self.sliced = False

        # Charger l'image si disponible
        self.image = None
        if image_path:
            if os.path.exists(image_path):
                try:
                    original_image = pygame.image.load(image_path)
                    # Redimensionner l'image
                    from config import FRUIT_IMAGE_SIZE
                    self.image = pygame.transform.scale(
                        original_image,
                        (FRUIT_IMAGE_SIZE, FRUIT_IMAGE_SIZE)
                    )
                    print(f"✓ Image chargée: {os.path.basename(image_path)}")
                except Exception as e:
                    print(f"✗ Erreur lors du chargement de {image_path}: {e}")
                    self.image = None
            else:
                print(f"✗ Fichier introuvable: {image_path}")

    def update(self):
        self.y += self.speed

    def draw(self, screen, font):
        if self.image:
            # Afficher l'image
            screen.blit(self.image, (self.x, self.y))
            # Afficher le mot en dessous de l'image
            text = font.render(self.word, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.x + self.image.get_width() // 2,
                                              self.y + self.image.get_height() + 15))

            # Fond semi-transparent pour le texte
            text_bg = pygame.Surface((text.get_width() + 10, text.get_height() + 5))
            text_bg.set_alpha(150)
            text_bg.fill((0, 0, 0))
            screen.blit(text_bg, (text_rect.x - 5, text_rect.y - 2))
            screen.blit(text, text_rect)
        else:
            # Fallback: afficher seulement le texte (avec un indicateur visuel)
            text = font.render(f"[{self.word}]", True, (255, 200, 0))
            screen.blit(text, (self.x, self.y))

    def is_off_screen(self, height):
        return self.y > height

    def get_rect(self):
        """Retourne le rectangle de collision"""
        if self.image:
            from config import FRUIT_IMAGE_SIZE
            return pygame.Rect(self.x, self.y, FRUIT_IMAGE_SIZE, FRUIT_IMAGE_SIZE)
        else:
            return pygame.Rect(self.x, self.y, 100, 30)