import pygame


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 400
        self.y = 50
        self.boss1 = pygame.image.load("data/boss1.png")
        self.boss2 = pygame.image.load("data/boss2.png")
        self.boss3 = pygame.image.load("data/boss3.png")
        self.boss4 = pygame.image.load("data/boss4.png")
        self.speed = 5
        self.change = self.speed
        self.yChange = 30
        self.life = 50
        self.newlife = 100
        self.damage = 7
        self.dead = False
        self.kill = 65
        self.rect = pygame.Rect(self.x, self.y, 130, 140)

    def movement(self):
        self.x += self.change
        self.rect = pygame.Rect(self.x, self.y, 130, 140)
        if self.x <= 0:
            self.change = self.speed
            self.y += self.yChange
        elif self.x >= 670:
            self.change = -self.speed
            self.y += self.yChange
