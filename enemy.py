import pygame
import random
from random import *


class smallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemy0.png").convert_alpha()
        self.destory_images = []
        self.destory_images.extend([ \
            pygame.image.load("image/enemy0_down1.png").convert_alpha(), \
            pygame.image.load("image/enemy0_down2.png").convert_alpha(), \
            pygame.image.load("image/enemy0_down3.png").convert_alpha(), \
            pygame.image.load("image/enemy0_down4.png").convert_alpha() \
            ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.life = True
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-5 * self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)  # 该模块将碰撞检测中的矩形选框变为除白色以外选框

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.life = True
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-5 * self.height, 0)


class midEnemy(pygame.sprite.Sprite):
    energy = 8  # 血条控制

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemy1.png").convert_alpha()
        self.image1 = pygame.image.load("image/enemy1_hit.png").convert_alpha()
        self.destory_images = []
        self.destory_images.extend([ \
            pygame.image.load("image/enemy1_down1.png").convert_alpha(), \
            pygame.image.load("image/enemy1_down2.png").convert_alpha(), \
            pygame.image.load("image/enemy1_down3.png").convert_alpha(), \
            pygame.image.load("image/enemy1_down4.png").convert_alpha() \
            ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.life = True
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image)  # 该模块将碰撞检测中的矩形选框变为除白色以外选框
        self.energy = midEnemy.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.life = True
        self.energy = bigEnemy.energy
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, -self.height)


class bigEnemy(pygame.sprite.Sprite):
    energy = 20

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("image/enemy2.png").convert_alpha()
        self.image2 = pygame.image.load("image/enemy2_n2.png").convert_alpha()
        self.image3 = pygame.image.load("image/enemy2_hit.png").convert_alpha()

        self.destory_images = []
        self.destory_images.extend([ \
            pygame.image.load("image/enemy2_down1.png").convert_alpha(), \
            pygame.image.load("image/enemy2_down2.png").convert_alpha(), \
            pygame.image.load("image/enemy2_down3.png").convert_alpha(), \
            pygame.image.load("image/enemy2_down4.png").convert_alpha(), \
            pygame.image.load("image/enemy2_down5.png").convert_alpha(), \
            pygame.image.load("image/enemy2_down6.png").convert_alpha() \
            ])
        #self.rect = self.image1.get_rect()
        self.rect = self.image2.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.life = True
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-15 * self.height, -5 * self.height)
        self.mask = pygame.mask.from_surface(self.image1)  # 该模块将碰撞检测中的矩形选框变为除白色以外选框
        self.energy = bigEnemy.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.life = True
        self.energy = bigEnemy.energy
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-15 * self.height, -5 * self.height)
