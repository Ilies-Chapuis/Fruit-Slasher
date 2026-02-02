import pygame
import os


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

    def update(self):
        self.y += self.speed

    def draw(self, screen, font):
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

    def is_off_screen(self, height):
        return self.y > height

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