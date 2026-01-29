class Player:
    def __init__(self, lives):
        self.score = 0
        self.lives = lives
        self.combo = 0

    def add_score(self):
        self.combo += 1
        bonus = 1 + self.combo // 5
        self.score += bonus

    def lose_life(self):
        self.lives -= 1
        self.combo = 0

    def reset_combo(self):
        self.combo = 0

    def alive(self):
        return self.lives > 0
    
    def history():