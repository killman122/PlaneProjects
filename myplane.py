import pygame


class Myplane(pygame.sprite.Sprite):  # 这里用作碰撞检测
    def __init__(self, bg_size):  # 约束飞机不跑出地图,初始化属性
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("image/hero1.png").convert_alpha()
        self.image2 = pygame.image.load("image/hero2.png").convert_alpha()
        self.destory_images = []  # 采用元组的方式存储毁灭的图片
        self.destory_images.extend([ \
            pygame.image.load("image/hero_blowup_n1.png").convert_alpha(), \
            pygame.image.load("image/hero_blowup_n2.png").convert_alpha(), \
            pygame.image.load("image/hero_blowup_n3.png").convert_alpha(), \
            pygame.image.load("image/hero_blowup_n4.png").convert_alpha() \
            ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, \
            self.height - self.rect.height
        # - 20
        self.speed = 10  # 设置飞机速度
        self.life = True
        self.mask = pygame.mask.from_surface(self.image1)  # 该模块将碰撞检测中的矩形选框变为除白色以外选框
        self.wudi = False

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0  # 设置移动的高度上限为0,限制在地图区域内活动

    def moveDown(self):
        if self.rect.bottom < self.height - 20:  # 设置底部在60px以内
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 20

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, \
            self.height - self.rect.height - 20
        self.life = True
        self.wudi = True
