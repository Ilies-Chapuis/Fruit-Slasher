import pygame

class Button:
    def __init__(self, text, x, y, w, h, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

    def draw(self, screen, font):
        pygame.draw.rect(screen, (60, 60, 60), self.rect, border_radius=8)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2, border_radius=8)

        txt = font.render(self.text, True, (255, 255, 255))
        screen.blit(
            txt,
            txt.get_rect(center=self.rect.center)
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
