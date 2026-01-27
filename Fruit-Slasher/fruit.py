import random

class Fruit:
    def __init__(self, word, x, speed, is_bomb=False):
        self.word = word
        self.x = x
        self.y = -30
        self.speed = speed
        self.is_bomb = is_bomb
        self.sliced = False

    def update(self):
        self.y += self.speed

    def draw(self, screen, font):
        text = font.render(self.word, True, (255, 255, 255))
        screen.blit(text, (self.x, self.y))

    def is_off_screen(self, height):
        return self.y > height
