import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randint(0, 735)
        self.y = random.randint(50, 150)
        self.speed = 4
        self.direction = [self.speed, -self.speed]
        self.change = random.choice(self.direction)
        self.yChange = 50
        self.spaceship = pygame.image.load("data/enemy.png")
        self.rect = pygame.Rect(round(self.x), round(self.y), 65, 75)

    def movement(self):
        self.x += self.change
        self.rect = pygame.Rect(round(self.x), round(self.y), 65, 75)
        if self.x <= 0:
            self.change = self.speed
            self.y += self.yChange
        elif self.x >= 736:
            self.change = -self.speed
            self.y += self.yChange
