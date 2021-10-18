import pygame
from pygame import mixer
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.init()
        self.x = 600
        self.y = 480
        self.speed = 6
        self.change = 0
        self.life = 3
        self.left = False
        self.right = False
        self.spaceshipWhite = pygame.image.load("data/spaceshipWhite.png")
        self.spaceshipBlue = pygame.image.load("data/spaceshipBlue.png")
        self.spaceshipRed = pygame.image.load("data/spaceshipRed.png")
        self.explosion = pygame.image.load("data/explosion.png")
        self.rect = pygame.Rect(self.x, self.y, 65, 75)

    def movement(self):
        self.x += self.change
        self.rect = pygame.Rect(self.x, self.y, 65, 75)
        if self.left:
            self.change = -self.speed
        elif self.right:
            self.change = self.speed
        else:
            self.change = 0
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 480
        self.speed = 20
        self.sound = mixer.Sound("data/laser.wav")
        self.sound.set_volume(0.1)
        self.state = "ready"
        self.laser = pygame.image.load("data/laser.png")
        self.bullet = pygame.image.load("data/bullet.png")
        self.rect = pygame.Rect(self.x + 8, self.y + 15, 18, 35)

    def movement(self):
        self.rect = pygame.Rect(self.x + 8, self.y + 15, 18, 35)
        if self.state == "fire":
            self.y += -self.speed
        else:
            self.y = 480


class Life(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.extra_life_position = -250
        self.x = random.randint(0, 735)
        self.y = self.extra_life_position
        self.speed = 2.5
        self.image = pygame.image.load("data/heart.png")
        self.rect = pygame.Rect(self.x, self.y, 25, 30)

    def movement(self):
        self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, 25, 30)
