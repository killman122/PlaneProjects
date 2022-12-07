import pygame


class bullet1(pygame.sprite.Sprite):
    def __init__(self, positon):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = positon
        self.speed = 12
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, positon):
        self.rect.left, self.rect.top = positon
        self.active = True


class bullet2(pygame.sprite.Sprite):
    def __init__(self, positon):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/bullet2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = positon
        self.speed = 14
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, positon):
        self.rect.left, self.rect.top = positon
        self.active = True

class bullet3(pygame.sprite.Sprite):
    def __init__(self, positon):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = positon
        self.speed = 12
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, positon):
        self.rect.left, self.rect.top = positon
        self.active = True
