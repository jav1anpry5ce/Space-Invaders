import pygame
from pygame import mixer
import sys
import os
import time
import random
from Player import *
from Enemy import *
from Boss import *

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

player = Player()
bullet = Bullet()
boss = Boss()
extralife = Life()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load("data/background.png")
        self.FPS = 60
        mixer.music.load("data/background.wav")
        self.explosionSound = mixer.Sound("data/explosion.wav")
        self.explosionSound.set_volume(0.1)
        mixer.music.set_volume(0.3)
        mixer.music.play(-1)
        self.mute = False
        self.clock = pygame.time.Clock()
        self.enemy = pygame.sprite.Group()
        self.game_over = False
        self.enemies_spawned = False
        self.boss_spawned = False
        self.level = 9
        self.num_of_enemy = 7
        self.enemy_limit = 30
        self.enemy_speed_limit = 10
        self.enemy_change_limit = 75
        self.level_up = False
        self.newHighscore = False
        self.debugMode = False
        self.explosion = pygame.image.load("data/explosion.png")
        self.heart = pygame.image.load("data/heart.png")
        self.lifeSymbol = []
        self.scoreValue = 0
        self.fonts = {
            "scoreFont": pygame.font.Font("data/freesansbold.ttf", 32),
            "lifeFont": pygame.font.Font("data/freesansbold.ttf", 32),
            "welcomeText": pygame.font.Font("data/freesansbold.ttf", 44),
            "playInstruction": pygame.font.Font("data/freesansbold.ttf", 34),
            "currentHighscore": pygame.font.Font("data/freesansbold.ttf", 64),
            "instruction": pygame.font.Font("data/freesansbold.ttf", 22),
            "pausedText": pygame.font.Font("data/freesansbold.ttf", 64),
            "pausedInstruction": pygame.font.Font("data/freesansbold.ttf", 32),
            "overFont": pygame.font.Font("data/freesansbold.ttf", 64),
            "playAgain": pygame.font.Font("data/freesansbold.ttf", 24),
            "highscore": pygame.font.Font("data/freesansbold.ttf", 48),
            "fps": pygame.font.Font("data/freesansbold.ttf", 16),
            "bossHealth": pygame.font.Font("data/freesansbold.ttf", 32),
        }
        for i in range(player.life):
            self.lifeSymbol.append(self.heart)

    def spawn(self, num):
        for i in range(num):
            self.enemy.add(Enemy())

    def levels(self):
        print(len(self.enemy))
        for enemy in self.enemy:
            enemy.movement()
        if self.num_of_enemy >= self.enemy_limit:
            self.num_of_enemy = self.enemy_limit
        if self.enemies_spawned is False and self.boss_spawned is False:
            self.spawn(self.num_of_enemy)
            self.enemies_spawned = True
        if self.level_up:
            for enemy in self.enemy:
                enemy.speed += 0.5
                enemy.yChange += 1.5
                if enemy.speed >= self.enemy_speed_limit:
                    enemy.speed = self.enemy_speed_limit
                if enemy.yChange >= self.enemy_change_limit:
                    enemy.yChange = self.enemy_change_limit
            self.level_up = False
        if len(self.enemy) <= 0 and self.boss_spawned is False:
            self.level_up = True
            self.num_of_enemy += 3
            self.level += 1
            self.enemies_spawned = False
        if self.level == 10 or self.level == 30 or self.level == 50 or self.level == 75:
            self.enemy.empty()
            self.fightBoss()

    def mainMenu(self):
        self.screen.blit(self.background, (0, 0))
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu = False
                    if event.key == pygame.K_q:
                        sys.exit()
                        pygame.quit()
                    if event.key == pygame.K_m:
                        self.muteunmute()
            with open("data/score.txt", "r") as score:
                highscore = score.read()
            welcomeDisplay = self.fonts["welcomeText"].render(
                "WELCOME TO SPACE INVADERS", True, (255, 255, 255)
            )
            playDisplay = self.fonts["playInstruction"].render(
                "Press Enter to play and Q to quit", True, (255, 255, 255)
            )
            highscoreDisplay = self.fonts["currentHighscore"].render(
                "Highscore : " + str(highscore), True, (255, 255, 255)
            )
            instructionDisplay = self.fonts["instruction"].render(
                "Press space to fire, left key to move left and right key to move right.",
                True,
                (255, 255, 255),
            )
            self.screen.blit(welcomeDisplay, (50, 100))
            self.screen.blit(playDisplay, (120, 170))
            self.screen.blit(highscoreDisplay, (150, 230))
            self.screen.blit(instructionDisplay, (50, 500))
            pygame.display.update()

    def pause(self):
        paused = True
        while paused:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                        # pygame.display.update()
                    if event.key == pygame.K_q:
                        sys.exit()
                        pygame.quit()
                    if event.key == pygame.K_m:
                        self.muteunmute()
            pausedDisplay = self.fonts["pausedText"].render(
                "GAME PAUSED", True, (255, 255, 255)
            )
            instructionDisplay = self.fonts["pausedInstruction"].render(
                "Press ecs to continue and Q to quit", True, (255, 255, 255)
            )
            self.screen.blit(pausedDisplay, (160, 250))
            self.screen.blit(instructionDisplay, (135, 350))
            pygame.display.update()

    def gameOver(self):
        if self.game_over:
            self.enemy.empty()
            over = self.fonts["overFont"].render("GAME OVER", True, (255, 255, 255))
            playAgain = self.fonts["playAgain"].render(
                "Press Enter to play again", True, (255, 255, 255)
            )
            newHighscore = self.fonts["highscore"].render(
                "NEW HIGHSCORE!!", True, (255, 255, 255)
            )
            self.screen.blit(over, (200, 230))
            self.screen.blit(playAgain, (260, 300))
            with open("data/score.txt", "r") as score:
                highscore = score.read()
                highscore = int(highscore)
                if self.scoreValue >= highscore:
                    self.newHighscore = True
                    self.screen.blit(newHighscore, (175, 150))
                    if self.newHighscore:
                        with open("data/score.txt", "w") as score:
                            score.write(str(self.scoreValue))
                            self.newHighscore = False

    def muteunmute(self):
        if self.mute == False:
            mixer.music.pause()
            bullet.sound.set_volume(0)
            self.explosionSound.set_volume(0)
            self.mute = True
        else:
            mixer.music.unpause()
            bullet.sound.set_volume(0.1)
            self.explosionSound.set_volume(0.1)
            self.mute = False

    def onScreenText(self):
        life = self.fonts["lifeFont"].render("Life: ", True, (255, 255, 255))
        score = self.fonts["scoreFont"].render(
            "Score: " + str(self.scoreValue), True, (255, 255, 255)
        )
        bossHealth = self.fonts["bossHealth"].render(
            "Health: " + str(boss.life), True, (255, 255, 255)
        )
        self.screen.blit(score, (320, 10))
        self.screen.blit(life, (10, 10))
        if self.boss_spawned:
            self.screen.blit(bossHealth, (610, 10))
        if player.life == 3:
            self.screen.blit(self.lifeSymbol[0], (85, 20))
            self.screen.blit(self.lifeSymbol[1], (115, 20))
            self.screen.blit(self.lifeSymbol[2], (145, 20))
        elif player.life == 2:
            self.screen.blit(self.lifeSymbol[0], (85, 20))
            self.screen.blit(self.lifeSymbol[1], (115, 20))
        elif player.life == 1:
            self.screen.blit(self.lifeSymbol[0], (85, 20))
        else:
            self.screen.blit(life, (10, 10))

    def fightBoss(self):
        self.boss_spawned = True
        if self.level == 10:
            self.screen.blit(boss.boss1, (round(boss.x), round(boss.y)))
        elif self.level == 30:
            self.screen.blit(boss.boss2, (boss.x, boss.y))
        elif self.level == 50:
            self.screen.blit(boss.boss3, (boss.x, boss.y))
        elif self.level == 75:
            self.screen.blit(boss.boss4, (boss.x, boss.y))
        boss.movement()
        if self.debugMode and self.boss_spawned:
            pygame.draw.rect(self.screen, (0), boss.rect, 1)

        if boss.dead:
            self.explosionSound.play()
            boss.life = boss.newlife
            self.num_of_enemy = 7
            boss.dead = False
            self.boss_spawned = False
            self.level += 1
            self.level_up = True
            if boss.dead == False:
                self.scoreValue += boss.kill
                boss.x = 400
                boss.y = 50
                boss.speed += 1
                boss.damage += 3
                boss.newlife += 50
                player.speed += 0.4
                boss.kill += 15
                boss.yChange += 4

    def display(self):
        self.screen.blit(self.background, (0, 0))
        self.onScreenText()
        self.gameOver()
        if bullet.state == "fire":
            if self.scoreValue >= 0 and self.scoreValue <= 300:
                self.screen.blit(bullet.laser, (round(bullet.x), round(bullet.y) + 16))
            elif self.scoreValue > 300 and self.scoreValue <= 1000:
                self.screen.blit(bullet.bullet, (round(bullet.x), round(bullet.y) + 16))
            else:
                self.screen.blit(bullet.laser, (round(bullet.x), round(bullet.y) + 10))
                self.screen.blit(
                    bullet.bullet, (round(bullet.x) + 30, round(bullet.y) + 10)
                )
            if self.debugMode:
                pygame.draw.rect(self.screen, (0), bullet.rect, 1)
        if bullet.y < 0:
            bullet.state = "ready"
            bullet.y = 480
        for enemy in self.enemy:
            self.screen.blit(enemy.spaceship, (round(enemy.x), round(enemy.y)))
            if self.debugMode:
                pygame.draw.rect(self.screen, (0), enemy.rect, 1)
        if self.scoreValue >= 0 and self.scoreValue <= 300:
            self.screen.blit(player.spaceshipWhite, (round(player.x), round(player.y)))
        elif self.scoreValue > 300 and self.scoreValue <= 1000:
            self.screen.blit(player.spaceshipBlue, (round(player.x), round(player.y)))
        else:
            self.screen.blit(player.spaceshipRed, (round(player.x), round(player.y)))
        if self.debugMode:
            pygame.draw.rect(self.screen, (0), extralife.rect, 1)
            pygame.draw.rect(self.screen, (0, 0, 0), player.rect, 1)
            fpsText = self.clock.get_fps()
            fpsText = round(fpsText)
            frames = self.fonts["fps"].render(
                "FPS: " + str(fpsText), True, (255, 255, 255)
            )
            self.screen.blit(frames, (10, 60))
        if player.life < 3 and player.life != 0:
            self.screen.blit(extralife.image, (round(extralife.x), round(extralife.y)))
            extralife.movement()

    def collisions(self):
        for enemy in self.enemy:
            if pygame.sprite.collide_rect(bullet, enemy) and bullet.state == "fire":
                self.screen.blit(self.explosion, (round(enemy.x), round(enemy.y)))
                self.explosionSound.play()
                bullet.state = "ready"
                bullet.y = 480
                self.scoreValue += 1
                self.enemy.remove(enemy)
            if enemy.y >= 430:
                for enemy in self.enemy:
                    enemy.x = random.randint(0, 735)
                    enemy.y = random.randint(50, 150)
                player.life -= 1
        if pygame.sprite.collide_rect(bullet, boss) and self.boss_spawned:
            bullet.state = "ready"
            bullet.y = 480
            boss.life -= boss.damage
        if boss.y > 360:
            player.life = 0
        if boss.life <= 0:
            boss.dead = True
        if pygame.sprite.collide_rect(player, extralife):
            extralife.rect = pygame.Rect(extralife.x, extralife.y, 25, 30)
            extralife.x = random.randint(0, 735)
            extralife.y = extralife.extra_life_position
            if player.life < 3 and player.life != 3:
                player.life += 1

    def play(self):
        self.display()
        self.collisions()
        bullet.movement()
        player.movement()
        self.levels()
        if player.life <= 0:
            self.game_over = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.left = True
                elif event.key == pygame.K_RIGHT:
                    player.right = True
                if event.key == pygame.K_ESCAPE:
                    if self.game_over == False:
                        self.pause()
                if event.key == pygame.K_m:
                    self.muteunmute()
                if event.key == pygame.K_SPACE:
                    if bullet.state == "ready":
                        bullet.x = player.x + 16
                        bullet.state = "fire"
                        bullet.sound.play()
                if event.key == pygame.K_RETURN:
                    if self.game_over:
                        self.game_over = False
                        self.levels()
                        player.life = 3
                        player.speed = 6
                        boss.speed = 5
                        boss.y = 50
                        boss.x = 400
                        self.scoreValue = 0
                        for enemy in self.enemy:
                            enemy.speed = 4
                if event.key == pygame.K_F3:
                    if self.debugMode == False:
                        self.debugMode = True
                    else:
                        self.debugMode = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.left = False
                elif event.key == pygame.K_RIGHT:
                    player.right = False

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


game = Game()
game.mainMenu()
while True:
    game.play()
    pygame.display.update()
    game.clock.tick(game.FPS)
